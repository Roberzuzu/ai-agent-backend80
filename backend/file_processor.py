"""
Procesador de archivos para Cerebro AI
Soporta imágenes, PDFs, DOCX, Excel, CSV y más
"""

import os
import io
import base64
from typing import Dict, Any, Optional, List
from PIL import Image
import PyPDF2
from docx import Document
import pandas as pd
from openai import OpenAI
import httpx

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

class FileProcessor:
    """Procesa diferentes tipos de archivos"""
    
    SUPPORTED_IMAGES = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    SUPPORTED_DOCS = ['.pdf', '.docx', '.txt']
    SUPPORTED_DATA = ['.csv', '.xlsx', '.xls']
    
    @staticmethod
    async def process_file(file_content: bytes, filename: str, file_type: str) -> Dict[str, Any]:
        """
        Procesa un archivo y retorna información extraída
        """
        ext = os.path.splitext(filename)[1].lower()
        
        try:
            if ext in FileProcessor.SUPPORTED_IMAGES:
                return await FileProcessor._process_image(file_content, filename)
            elif ext in FileProcessor.SUPPORTED_DOCS:
                return await FileProcessor._process_document(file_content, filename, ext)
            elif ext in FileProcessor.SUPPORTED_DATA:
                return await FileProcessor._process_data_file(file_content, filename, ext)
            else:
                return {
                    "success": False,
                    "error": f"Tipo de archivo no soportado: {ext}",
                    "filename": filename
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "filename": filename
            }
    
    @staticmethod
    async def _process_image(file_content: bytes, filename: str) -> Dict[str, Any]:
        """Analiza una imagen usando Vision API de OpenAI"""
        try:
            # Abrir imagen con PIL para validar
            image = Image.open(io.BytesIO(file_content))
            width, height = image.size
            format = image.format
            
            # Convertir a base64 para OpenAI
            base64_image = base64.b64encode(file_content).decode('utf-8')
            
            # Analizar con GPT-4 Vision
            analysis = None
            if openai_client:
                try:
                    response = openai_client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": """Analiza esta imagen detalladamente. Si es un producto:
                                        - Describe el producto
                                        - Identifica características clave
                                        - Sugiere un nombre de producto
                                        - Sugiere un precio aproximado
                                        - Categoría recomendada
                                        - Keywords para SEO
                                        
                                        Si no es un producto, describe lo que ves."""
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ],
                        max_tokens=500
                    )
                    analysis = response.choices[0].message.content
                except Exception as e:
                    print(f"Error con Vision API: {e}")
                    analysis = "No se pudo analizar la imagen con IA"
            
            return {
                "success": True,
                "type": "image",
                "filename": filename,
                "format": format,
                "dimensions": {"width": width, "height": height},
                "size_bytes": len(file_content),
                "analysis": analysis,
                "base64": base64_image[:100] + "...",  # Preview
                "full_base64": base64_image  # Full para guardar
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Error procesando imagen: {str(e)}",
                "filename": filename
            }
    
    @staticmethod
    async def _process_document(file_content: bytes, filename: str, ext: str) -> Dict[str, Any]:
        """Extrae texto de documentos PDF, DOCX, TXT"""
        try:
            text = ""
            
            if ext == '.pdf':
                # Extraer texto de PDF
                pdf_file = io.BytesIO(file_content)
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                num_pages = len(pdf_reader.pages)
                
                for page_num in range(min(num_pages, 50)):  # Límite 50 páginas
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
            
            elif ext == '.docx':
                # Extraer texto de DOCX
                doc_file = io.BytesIO(file_content)
                doc = Document(doc_file)
                text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            elif ext == '.txt':
                # Texto plano
                text = file_content.decode('utf-8', errors='ignore')
            
            # Analizar el contenido con IA
            summary = None
            if openai_client and text.strip():
                try:
                    response = openai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "system",
                                "content": "Eres un asistente que resume documentos. Extrae la información clave y haz un resumen estructurado."
                            },
                            {
                                "role": "user",
                                "content": f"Resume este documento:\n\n{text[:4000]}"  # Límite de tokens
                            }
                        ],
                        max_tokens=500
                    )
                    summary = response.choices[0].message.content
                except Exception as e:
                    print(f"Error generando resumen: {e}")
                    summary = "No se pudo generar resumen"
            
            return {
                "success": True,
                "type": "document",
                "filename": filename,
                "format": ext,
                "text_length": len(text),
                "text_preview": text[:500] + "..." if len(text) > 500 else text,
                "full_text": text,
                "summary": summary,
                "size_bytes": len(file_content)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Error procesando documento: {str(e)}",
                "filename": filename
            }
    
    @staticmethod
    async def _process_data_file(file_content: bytes, filename: str, ext: str) -> Dict[str, Any]:
        """Procesa archivos CSV y Excel"""
        try:
            df = None
            
            if ext == '.csv':
                df = pd.read_csv(io.BytesIO(file_content))
            elif ext in ['.xlsx', '.xls']:
                df = pd.read_excel(io.BytesIO(file_content))
            
            if df is None:
                raise Exception("No se pudo cargar el archivo de datos")
            
            # Información básica
            info = {
                "success": True,
                "type": "data",
                "filename": filename,
                "format": ext,
                "rows": len(df),
                "columns": list(df.columns),
                "column_count": len(df.columns),
                "size_bytes": len(file_content),
                "data_types": df.dtypes.astype(str).to_dict(),
                "preview": df.head(10).to_dict(orient='records'),
                "summary_stats": {}
            }
            
            # Estadísticas para columnas numéricas
            numeric_cols = df.select_dtypes(include=['number']).columns
            for col in numeric_cols:
                info["summary_stats"][col] = {
                    "mean": float(df[col].mean()) if not df[col].isna().all() else None,
                    "median": float(df[col].median()) if not df[col].isna().all() else None,
                    "min": float(df[col].min()) if not df[col].isna().all() else None,
                    "max": float(df[col].max()) if not df[col].isna().all() else None
                }
            
            # Análisis con IA si es posible
            if openai_client:
                try:
                    analysis_prompt = f"""Analiza estos datos:
                    - Archivo: {filename}
                    - Filas: {len(df)}
                    - Columnas: {', '.join(df.columns)}
                    - Preview: {df.head(3).to_string()}
                    
                    Proporciona:
                    1. Qué tipo de datos contiene
                    2. Insights clave
                    3. Sugerencias de uso (si son productos, ventas, etc)"""
                    
                    response = openai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Eres un analista de datos experto."},
                            {"role": "user", "content": analysis_prompt}
                        ],
                        max_tokens=500
                    )
                    info["ai_analysis"] = response.choices[0].message.content
                except Exception as e:
                    print(f"Error en análisis IA: {e}")
                    info["ai_analysis"] = "No disponible"
            
            return info
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Error procesando archivo de datos: {str(e)}",
                "filename": filename
            }
    
    @staticmethod
    def is_supported(filename: str) -> bool:
        """Verifica si el archivo es soportado"""
        ext = os.path.splitext(filename)[1].lower()
        return ext in (
            FileProcessor.SUPPORTED_IMAGES + 
            FileProcessor.SUPPORTED_DOCS + 
            FileProcessor.SUPPORTED_DATA
        )
