import React, { useState, useEffect, useRef } from 'react';
import { 
  Bot, 
  Send, 
  Trash2, 
  Loader2, 
  Brain,
  Sparkles,
  AlertCircle,
  CheckCircle2,
  Clock,
  Paperclip,
  X,
  FileText,
  Image as ImageIcon,
  FileSpreadsheet,
  Download
} from 'lucide-react';
import axiosInstance from '../lib/axiosConfig';
import { toast } from 'sonner';

function CerebroAIPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [agentStatus, setAgentStatus] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [filePreview, setFilePreview] = useState(null);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);
  const userId = 'web_user_' + Date.now(); // En producción, usar el ID del usuario logueado

  useEffect(() => {
    loadAgentStatus();
    loadHistory();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadAgentStatus = async () => {
    try {
      const response = await axiosInstance.get('/agent/status');
      setAgentStatus(response.data);
    } catch (error) {
      console.error('Error loading agent status:', error);
    }
  };

  const loadHistory = async () => {
    try {
      const response = await axiosInstance.get(`/agent/memory/${userId}?limit=10`);
      if (response.data.success && response.data.memories) {
        const historyMessages = response.data.memories.flatMap(mem => [
          {
            type: 'user',
            content: mem.command,
            timestamp: mem.timestamp
          },
          {
            type: 'bot',
            content: typeof mem.response === 'string' ? mem.response : JSON.stringify(mem.response),
            timestamp: mem.timestamp,
            plan: mem.plan
          }
        ]);
        setMessages(historyMessages);
      }
    } catch (error) {
      console.error('Error loading history:', error);
    }
  };

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      
      // Crear preview para imágenes
      if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onloadend = () => {
          setFilePreview(reader.result);
        };
        reader.readAsDataURL(file);
      } else {
        setFilePreview(null);
      }
      
      toast.success(`Archivo seleccionado: ${file.name}`);
    }
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    setFilePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSend = async () => {
    if ((!input.trim() && !selectedFile) || loading) return;

    const userMessage = {
      type: 'user',
      content: input || (selectedFile ? `📎 ${selectedFile.name}` : ''),
      timestamp: new Date().toISOString(),
      hasFile: !!selectedFile,
      fileName: selectedFile?.name,
      filePreview: filePreview
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = input;
    const currentFile = selectedFile;
    setInput('');
    setSelectedFile(null);
    setFilePreview(null);
    setLoading(true);

    try {
      let response;
      
      // Si hay archivo, usar endpoint de upload
      if (currentFile) {
        const formData = new FormData();
        formData.append('file', currentFile);
        formData.append('user_id', userId);
        if (currentInput.trim()) {
          formData.append('command', currentInput);
        }

        response = await axiosInstance.post('/agent/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        
        // Estructura de respuesta diferente con archivos
        if (response.data.success) {
          let botContent = response.data.message || 'Archivo procesado';
          
          // Si hay respuesta del agente
          if (response.data.agent_response) {
            botContent = response.data.agent_response.mensaje;
          }
          
          const botMessage = {
            type: 'bot',
            content: botContent,
            timestamp: new Date().toISOString(),
            file_info: response.data.file_info,
            resultados: response.data.agent_response?.resultados,
            provider: 'perplexity'
          };
          setMessages(prev => [...prev, botMessage]);
          toast.success('Archivo procesado correctamente');
        }
      } else {
        // Sin archivo, usar endpoint normal
        response = await axiosInstance.post('/agent/execute', {
          command: currentInput,
          user_id: userId
        });

        if (response.data.success) {
          const botMessage = {
            type: 'bot',
            content: response.data.mensaje,
            timestamp: new Date().toISOString(),
            plan: response.data.plan,
            resultados: response.data.resultados,
            provider: response.data.provider
          };
          setMessages(prev => [...prev, botMessage]);
          toast.success('Comando ejecutado correctamente');
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        type: 'bot',
        content: `❌ Error: ${error.response?.data?.detail || error.message}`,
        timestamp: new Date().toISOString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
      toast.error('Error al ejecutar comando');
    } finally {
      setLoading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleClearHistory = () => {
    if (window.confirm('¿Estás seguro de que quieres limpiar el historial?')) {
      setMessages([]);
      toast.success('Historial limpiado');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('es-ES', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl">
                <Brain className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
                  Cerebro AI
                  {agentStatus?.agente_activo && (
                    <span className="flex items-center gap-1 text-sm font-normal text-green-600">
                      <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                      Activo
                    </span>
                  )}
                </h1>
                <p className="text-slate-600 text-sm">
                  {agentStatus?.modelo || 'Cargando...'} • {agentStatus?.herramientas_disponibles || 0} herramientas disponibles
                </p>
              </div>
            </div>
            <button
              onClick={handleClearHistory}
              className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            >
              <Trash2 className="w-4 h-4" />
              Limpiar historial
            </button>
          </div>
        </div>

        {/* Chat Container */}
        <div className="bg-white rounded-xl shadow-sm overflow-hidden">
          {/* Messages */}
          <div className="overflow-y-auto p-6 space-y-4" style={{ height: 'calc(100vh - 400px)' }}>
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center">
                <div className="p-4 bg-gradient-to-br from-blue-50 to-purple-50 rounded-full mb-4">
                  <Sparkles className="w-12 h-12 text-blue-600" />
                </div>
                <h3 className="text-xl font-semibold text-slate-800 mb-2">
                  ¡Hola! Soy Cerebro AI
                </h3>
                <p className="text-slate-600 max-w-md">
                  Puedo ayudarte con análisis, productos, marketing y mucho más.
                  Escribe tu comando abajo para comenzar.
                </p>
                <div className="mt-6 grid grid-cols-2 gap-3 max-w-2xl">
                  <button
                    onClick={() => setInput('Dame las estadísticas del sitio')}
                    className="p-3 bg-blue-50 hover:bg-blue-100 rounded-lg text-sm text-left transition-colors"
                  >
                    📊 Ver estadísticas
                  </button>
                  <button
                    onClick={() => setInput('¿Cuántos productos tengo?')}
                    className="p-3 bg-purple-50 hover:bg-purple-100 rounded-lg text-sm text-left transition-colors"
                  >
                    🛍️ Ver productos
                  </button>
                  <button
                    onClick={() => setInput('Analiza las tendencias de mercado')}
                    className="p-3 bg-green-50 hover:bg-green-100 rounded-lg text-sm text-left transition-colors"
                  >
                    📈 Analizar tendencias
                  </button>
                  <button
                    onClick={() => setInput('Genera contenido para redes sociales')}
                    className="p-3 bg-orange-50 hover:bg-orange-100 rounded-lg text-sm text-left transition-colors"
                  >
                    ✨ Crear contenido
                  </button>
                </div>
              </div>
            ) : (
              <>
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex gap-3 ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    {message.type === 'bot' && (
                      <div className="flex-shrink-0">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                          <Bot className="w-5 h-5 text-white" />
                        </div>
                      </div>
                    )}
                    <div className={`flex flex-col gap-1 max-w-2xl ${message.type === 'user' ? 'items-end' : 'items-start'}`}>
                      <div
                        className={`rounded-2xl px-4 py-3 ${
                          message.type === 'user'
                            ? 'bg-gradient-to-br from-blue-600 to-purple-600 text-white'
                            : message.isError
                            ? 'bg-red-50 text-red-800 border border-red-200'
                            : 'bg-slate-100 text-slate-800'
                        }`}
                      >
                        {/* Show file preview for user messages with files */}
                        {message.hasFile && message.filePreview && (
                          <div className="mb-2">
                            <img 
                              src={message.filePreview} 
                              alt="Uploaded" 
                              className="max-w-xs rounded-lg"
                            />
                          </div>
                        )}
                        
                        <p className="whitespace-pre-wrap">{message.content}</p>
                        
                        {/* Show file info from bot response */}
                        {message.file_info && (
                          <div className="mt-3 pt-3 border-t border-slate-200">
                            <p className="text-xs font-semibold mb-2 text-slate-600">📄 Información del archivo:</p>
                            <div className="p-2 bg-white rounded-lg text-sm">
                              <p className="text-slate-700">
                                <strong>Tipo:</strong> {message.file_info.type}
                              </p>
                              {message.file_info.analysis && (
                                <div className="mt-2">
                                  <p className="text-slate-700 font-medium">Análisis:</p>
                                  <p className="text-slate-600 text-xs mt-1">{message.file_info.analysis}</p>
                                </div>
                              )}
                              {message.file_info.summary && (
                                <div className="mt-2">
                                  <p className="text-slate-700 font-medium">Resumen:</p>
                                  <p className="text-slate-600 text-xs mt-1">{message.file_info.summary}</p>
                                </div>
                              )}
                              {message.file_info.ai_analysis && (
                                <div className="mt-2">
                                  <p className="text-slate-700 font-medium">Análisis IA:</p>
                                  <p className="text-slate-600 text-xs mt-1">{message.file_info.ai_analysis}</p>
                                </div>
                              )}
                            </div>
                          </div>
                        )}
                        
                        {/* Show results if available */}
                        {message.resultados && message.resultados.length > 0 && (
                          <div className="mt-3 pt-3 border-t border-slate-200">
                            <p className="text-xs font-semibold mb-2 text-slate-600">Resultados:</p>
                            {message.resultados.map((resultado, idx) => (
                              <div key={idx} className="mb-2 p-2 bg-white rounded-lg text-sm">
                                <p className="font-medium text-slate-700 mb-1">
                                  🛠️ {resultado.herramienta}
                                </p>
                                <pre className="text-xs text-slate-600 overflow-x-auto">
                                  {JSON.stringify(resultado.resultado, null, 2)}
                                </pre>
                              </div>
                            ))}
                          </div>
                        )}

                        {/* Provider badge */}
                        {message.provider && (
                          <div className="mt-2 flex items-center gap-1">
                            <span className="text-xs px-2 py-0.5 bg-white/20 rounded-full">
                              🧠 {message.provider}
                            </span>
                          </div>
                        )}
                      </div>
                      <span className="text-xs text-slate-500 px-2">
                        {formatTimestamp(message.timestamp)}
                      </span>
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="flex gap-3 justify-start">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                        <Bot className="w-5 h-5 text-white" />
                      </div>
                    </div>
                    <div className="bg-slate-100 rounded-2xl px-4 py-3">
                      <div className="flex items-center gap-2">
                        <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
                        <span className="text-slate-600">Pensando...</span>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </>
            )}
          </div>

          {/* Input */}
          <div className="border-t border-slate-200 p-4 bg-slate-50">
            {/* File preview if selected */}
            {selectedFile && (
              <div className="mb-3 p-3 bg-white border border-slate-200 rounded-lg flex items-center justify-between">
                <div className="flex items-center gap-3">
                  {filePreview ? (
                    <img src={filePreview} alt="Preview" className="w-12 h-12 object-cover rounded" />
                  ) : (
                    <div className="w-12 h-12 bg-slate-100 rounded flex items-center justify-center">
                      {selectedFile.type.includes('pdf') ? (
                        <FileText className="w-6 h-6 text-red-500" />
                      ) : selectedFile.type.includes('sheet') || selectedFile.type.includes('excel') || selectedFile.name.endsWith('.csv') ? (
                        <FileSpreadsheet className="w-6 h-6 text-green-500" />
                      ) : selectedFile.type.includes('document') ? (
                        <FileText className="w-6 h-6 text-blue-500" />
                      ) : (
                        <FileText className="w-6 h-6 text-slate-500" />
                      )}
                    </div>
                  )}
                  <div>
                    <p className="text-sm font-medium text-slate-800">{selectedFile.name}</p>
                    <p className="text-xs text-slate-500">
                      {(selectedFile.size / 1024).toFixed(2)} KB
                    </p>
                  </div>
                </div>
                <button
                  onClick={handleRemoveFile}
                  className="p-1 hover:bg-slate-100 rounded transition-colors"
                >
                  <X className="w-5 h-5 text-slate-500" />
                </button>
              </div>
            )}
            
            <div className="flex gap-3">
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileSelect}
                className="hidden"
                accept="image/*,.pdf,.docx,.xlsx,.xls,.csv,.txt"
              />
              
              <button
                onClick={() => fileInputRef.current?.click()}
                disabled={loading}
                className="px-4 py-3 bg-blue-50 border border-blue-300 rounded-xl hover:bg-blue-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
                title="Adjuntar archivo"
              >
                <Paperclip className="w-5 h-5 text-blue-600" />
                <span className="text-sm font-medium text-blue-600">Archivo</span>
              </button>
              
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={selectedFile ? "Escribe un comando para el archivo..." : "Escribe tu comando aquí..."}
                className="flex-1 px-4 py-3 bg-white border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={loading}
              />
              <button
                onClick={handleSend}
                disabled={loading || (!input.trim() && !selectedFile)}
                className="px-6 py-3 bg-gradient-to-br from-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2 font-medium"
              >
                {loading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <Send className="w-5 h-5" />
                )}
                Enviar
              </button>
            </div>
            <p className="text-xs text-slate-500 mt-2">
              💡 Tip: Sube una imagen de producto para analizarla y crear el producto automáticamente
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CerebroAIPage;
