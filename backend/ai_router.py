import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import re
from typing import Optional, Dict, Any

router = APIRouter()

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
FAL_API_KEY = os.getenv("FAL_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ABACUS_API_KEY = os.getenv("ABACUS_API_KEY")

# Request/Response Models
class QueryRequest(BaseModel):
    query: str
    context: Optional[str] = None
    preferred_model: Optional[str] = None

class AIResponse(BaseModel):
    response: str
    platform: str
    model_used: str
    confidence: float

# Intent Detection Functions
def detect_intent(query: str) -> Dict[str, Any]:
    """
    Analyze query to determine the best AI platform to use.
    Returns: {"platform": str, "confidence": float, "reasoning": str}
    """
    query_lower = query.lower()
    
    # Image generation patterns
    image_keywords = ["generate image", "create image", "draw", "picture of", 
                     "generate picture", "make an image", "visualize", "illustrate"]
    if any(keyword in query_lower for keyword in image_keywords):
        return {"platform": "fal", "confidence": 0.95, "reasoning": "Image generation request"}
    
    # Search/Research patterns
    search_keywords = ["search", "find information", "look up", "research", 
                      "current", "latest", "news about", "what happened", 
                      "when did", "who is", "real-time"]
    if any(keyword in query_lower for keyword in search_keywords):
        return {"platform": "perplexity", "confidence": 0.90, "reasoning": "Search/research query"}
    
    # Analytics/Data patterns
    analytics_keywords = ["analyze data", "statistics", "metrics", "trend analysis",
                         "predict", "forecast", "data insights", "correlation",
                         "regression", "classification"]
    if any(keyword in query_lower for keyword in analytics_keywords):
        return {"platform": "abacus", "confidence": 0.88, "reasoning": "Analytics/data analysis"}
    
    # GPT-4 specialized patterns (code, complex reasoning)
    gpt4_keywords = ["write code", "debug", "programming", "algorithm",
                    "explain code", "refactor", "optimize code"]
    if any(keyword in query_lower for keyword in gpt4_keywords):
        return {"platform": "openai", "confidence": 0.85, "reasoning": "Code/technical task"}
    
    # Default to Claude (OpenRouter) for general conversation
    return {"platform": "openrouter", "confidence": 0.70, "reasoning": "General conversation"}

# Platform-specific API calls
async def call_openrouter(query: str, context: Optional[str] = None) -> Dict[str, Any]:
    """Route query to Claude via OpenRouter"""
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="OpenRouter API key not configured")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "anthropic/claude-3.5-sonnet",
                    "messages": [
                        {"role": "system", "content": context or "You are a helpful AI assistant."},
                        {"role": "user", "content": query}
                    ]
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            return {
                "response": data["choices"][0]["message"]["content"],
                "model": "claude-3.5-sonnet"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenRouter error: {str(e)}")

async def call_perplexity(query: str, context: Optional[str] = None) -> Dict[str, Any]:
    """Route search queries to Perplexity"""
    if not PERPLEXITY_API_KEY:
        raise HTTPException(status_code=500, detail="Perplexity API key not configured")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-sonar-large-128k-online",
                    "messages": [
                        {"role": "system", "content": context or "Provide accurate, up-to-date information."},
                        {"role": "user", "content": query}
                    ]
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            return {
                "response": data["choices"][0]["message"]["content"],
                "model": "llama-3.1-sonar-large-128k-online"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Perplexity error: {str(e)}")

async def call_fal(query: str, context: Optional[str] = None) -> Dict[str, Any]:
    """Route image generation to Fal AI"""
    if not FAL_API_KEY:
        raise HTTPException(status_code=500, detail="Fal API key not configured")
    
    # Extract image prompt from query
    prompt = re.sub(r'^(generate|create|draw|make)\s+(an?\s+)?(image|picture)\s+(of\s+)?', '', query, flags=re.IGNORECASE).strip()
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://fal.run/fal-ai/flux/schnell",
                headers={
                    "Authorization": f"Key {FAL_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "prompt": prompt,
                    "image_size": "landscape_16_9",
                    "num_inference_steps": 4,
                    "num_images": 1
                },
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
            return {
                "response": f"Image generated successfully. URL: {data['images'][0]['url']}",
                "model": "flux-schnell",
                "image_url": data['images'][0]['url']
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Fal AI error: {str(e)}")

async def call_openai(query: str, context: Optional[str] = None) -> Dict[str, Any]:
    """Route query to OpenAI GPT-4"""
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4-turbo-preview",
                    "messages": [
                        {"role": "system", "content": context or "You are an expert coding assistant."},
                        {"role": "user", "content": query}
                    ]
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            return {
                "response": data["choices"][0]["message"]["content"],
                "model": "gpt-4-turbo-preview"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")

async def call_abacus(query: str, context: Optional[str] = None) -> Dict[str, Any]:
    """Route analytics queries to Abacus AI"""
    if not ABACUS_API_KEY:
        raise HTTPException(status_code=500, detail="Abacus API key not configured")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://api.abacus.ai/v1/chat",
                headers={
                    "Authorization": f"Bearer {ABACUS_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "abacus-analytics",
                    "messages": [
                        {"role": "system", "content": context or "You are a data analytics expert."},
                        {"role": "user", "content": query}
                    ]
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            return {
                "response": data["response"],
                "model": "abacus-analytics"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Abacus AI error: {str(e)}")

# Main routing endpoint
@router.post("/query", response_model=AIResponse)
async def route_query(request: QueryRequest):
    """
    Intelligent AI router that automatically selects the best platform.
    """
    # Detect intent
    intent = detect_intent(request.query)
    
    # Override with preferred model if specified
    platform = request.preferred_model or intent["platform"]
    
    # Route to appropriate platform
    platform_handlers = {
        "openrouter": call_openrouter,
        "perplexity": call_perplexity,
        "fal": call_fal,
        "openai": call_openai,
        "abacus": call_abacus
    }
    
    if platform not in platform_handlers:
        raise HTTPException(status_code=400, detail=f"Unknown platform: {platform}")
    
    # Call the selected platform
    try:
        result = await platform_handlers[platform](request.query, request.context)
        
        return AIResponse(
            response=result["response"],
            platform=platform,
            model_used=result["model"],
            confidence=intent["confidence"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Routing error: {str(e)}")

@router.get("/health")
async def health_check():
    """Check which AI platforms are configured"""
    return {
        "status": "healthy",
        "platforms": {
            "openrouter": bool(OPENROUTER_API_KEY),
            "perplexity": bool(PERPLEXITY_API_KEY),
            "fal": bool(FAL_API_KEY),
            "openai": bool(OPENAI_API_KEY),
            "abacus": bool(ABACUS_API_KEY)
        }
    }
