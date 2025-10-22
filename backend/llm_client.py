"""
Standalone LLM Client - Replace emergentintegrations.llm.chat
Supports OpenAI, Anthropic, and other providers natively
"""

import os
from typing import Optional, Dict, Any, List
from openai import OpenAI, AsyncOpenAI
from anthropic import Anthropic, AsyncAnthropic
import httpx


class Message:
    """Simple message wrapper"""
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content


class UserMessage:
    """User message wrapper for compatibility"""
    def __init__(self, text: str):
        self.text = text


class LlmChat:
    """Standalone LLM chat client - replaces emergentintegrations"""
    
    def __init__(self, api_key: str, session_id: str, system_message: str = ""):
        self.api_key = api_key
        self.session_id = session_id
        self.system_message = system_message
        self.provider = "openai"  # default
        self.model = "gpt-4o"
        self.messages = []
        
        if system_message:
            self.messages.append({"role": "system", "content": system_message})
    
    def with_model(self, provider: str, model: str):
        """Set provider and model"""
        self.provider = provider.lower()
        self.model = model
        return self
    
    async def send_message(self, user_message: UserMessage) -> str:
        """Send message and get response"""
        # Add user message
        self.messages.append({"role": "user", "content": user_message.text})
        
        # Call appropriate provider
        if self.provider == "openai":
            response = await self._call_openai()
        elif self.provider == "anthropic":
            response = await self._call_anthropic()
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
        
        # Add assistant response
        self.messages.append({"role": "assistant", "content": response})
        
        return response
    
    async def _call_openai(self) -> str:
        """Call OpenAI API"""
        client = AsyncOpenAI(api_key=self.api_key)
        
        response = await client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    async def _call_anthropic(self) -> str:
        """Call Anthropic API"""
        client = AsyncAnthropic(api_key=self.api_key)
        
        # Extract system message if present
        system_msg = ""
        conv_messages = []
        
        for msg in self.messages:
            if msg["role"] == "system":
                system_msg = msg["content"]
            else:
                conv_messages.append(msg)
        
        response = await client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=system_msg,
            messages=conv_messages
        )
        
        return response.content[0].text
