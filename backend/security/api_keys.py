"""
API Key Management System
Handles API key generation, rotation, validation, and scopes
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone, timedelta
import secrets
import hashlib
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

logger = logging.getLogger(__name__)


class APIKey(BaseModel):
    """API Key model"""
    id: str
    user_email: str
    name: str  # Friendly name for the key
    key_hash: str  # Hashed version of the key
    key_prefix: str  # First 8 chars for identification
    scopes: List[str] = []  # Permissions/scopes
    is_active: bool = True
    expires_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    usage_count: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = {}


class APIKeyCreate(BaseModel):
    """Request model for creating API key"""
    name: str
    scopes: List[str] = []
    expires_in_days: Optional[int] = None  # None = no expiration
    metadata: Dict[str, Any] = {}


class APIKeyManager:
    """Manage API keys with rotation and validation"""
    
    # Available scopes
    AVAILABLE_SCOPES = [
        "read:products",
        "write:products",
        "read:analytics",
        "read:payments",
        "write:payments",
        "read:subscriptions",
        "write:subscriptions",
        "read:affiliates",
        "write:affiliates",
        "read:notifications",
        "write:notifications",
        "admin:all"
    ]
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db['api_keys']
    
    @staticmethod
    def generate_api_key() -> str:
        """
        Generate a secure API key
        Format: emergent_live_<32_random_chars>
        """
        random_part = secrets.token_urlsafe(32)
        return f"emergent_live_{random_part}"
    
    @staticmethod
    def hash_api_key(api_key: str) -> str:
        """Hash API key for secure storage"""
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    @staticmethod
    def get_key_prefix(api_key: str) -> str:
        """Get first 12 chars for display"""
        return api_key[:12] if len(api_key) >= 12 else api_key
    
    async def create_api_key(
        self,
        user_email: str,
        name: str,
        scopes: List[str] = None,
        expires_in_days: int = None,
        metadata: Dict[str, Any] = None
    ) -> tuple[APIKey, str]:
        """
        Create a new API key
        Returns (APIKey object, plain_text_key)
        """
        # Generate key
        plain_key = self.generate_api_key()
        key_hash = self.hash_api_key(plain_key)
        key_prefix = self.get_key_prefix(plain_key)
        
        # Calculate expiration
        expires_at = None
        if expires_in_days:
            expires_at = datetime.now(timezone.utc) + timedelta(days=expires_in_days)
        
        # Validate scopes
        scopes = scopes or []
        invalid_scopes = [s for s in scopes if s not in self.AVAILABLE_SCOPES]
        if invalid_scopes:
            raise ValueError(f"Invalid scopes: {invalid_scopes}")
        
        # Create API key object
        api_key = APIKey(
            id=secrets.token_urlsafe(16),
            user_email=user_email,
            name=name,
            key_hash=key_hash,
            key_prefix=key_prefix,
            scopes=scopes,
            expires_at=expires_at,
            metadata=metadata or {}
        )
        
        # Save to database
        await self.collection.insert_one(api_key.model_dump())
        
        logger.info(f"Created API key '{name}' for {user_email}")
        
        # Return both object and plain key (only time plain key is visible)
        return api_key, plain_key
    
    async def validate_api_key(
        self,
        api_key: str,
        required_scopes: List[str] = None
    ) -> Optional[APIKey]:
        """
        Validate API key and check scopes
        Returns APIKey object if valid, None otherwise
        """
        # Hash the provided key
        key_hash = self.hash_api_key(api_key)
        
        # Find key in database
        key_data = await self.collection.find_one({
            'key_hash': key_hash,
            'is_active': True
        })
        
        if not key_data:
            logger.warning("Invalid API key attempted")
            return None
        
        api_key_obj = APIKey(**key_data)
        
        # Check expiration
        if api_key_obj.expires_at:
            if datetime.now(timezone.utc) > api_key_obj.expires_at:
                logger.warning(f"Expired API key used: {api_key_obj.key_prefix}")
                return None
        
        # Check scopes
        if required_scopes:
            # If key has admin:all scope, allow everything
            if "admin:all" not in api_key_obj.scopes:
                missing_scopes = [s for s in required_scopes if s not in api_key_obj.scopes]
                if missing_scopes:
                    logger.warning(
                        f"API key {api_key_obj.key_prefix} missing scopes: {missing_scopes}"
                    )
                    return None
        
        # Update usage stats
        await self.collection.update_one(
            {'id': api_key_obj.id},
            {
                '$set': {'last_used_at': datetime.now(timezone.utc)},
                '$inc': {'usage_count': 1}
            }
        )
        
        return api_key_obj
    
    async def list_api_keys(self, user_email: str) -> List[APIKey]:
        """List all API keys for a user (excluding sensitive data)"""
        cursor = self.collection.find(
            {'user_email': user_email},
            {'key_hash': 0}  # Exclude hash from results
        ).sort('created_at', -1)
        
        keys = await cursor.to_list(length=100)
        return [APIKey(**k) for k in keys]
    
    async def revoke_api_key(self, key_id: str, user_email: str) -> bool:
        """Revoke (deactivate) an API key"""
        result = await self.collection.update_one(
            {'id': key_id, 'user_email': user_email},
            {
                '$set': {
                    'is_active': False,
                    'updated_at': datetime.now(timezone.utc)
                }
            }
        )
        
        if result.modified_count > 0:
            logger.info(f"Revoked API key {key_id} for {user_email}")
            return True
        return False
    
    async def rotate_api_key(
        self,
        key_id: str,
        user_email: str
    ) -> tuple[APIKey, str]:
        """
        Rotate an API key (create new, revoke old)
        Returns (new_APIKey, plain_text_key)
        """
        # Get old key
        old_key = await self.collection.find_one({
            'id': key_id,
            'user_email': user_email
        })
        
        if not old_key:
            raise ValueError("API key not found")
        
        old_key_obj = APIKey(**old_key)
        
        # Create new key with same properties
        new_key, plain_key = await self.create_api_key(
            user_email=user_email,
            name=f"{old_key_obj.name} (rotated)",
            scopes=old_key_obj.scopes,
            expires_in_days=(
                (old_key_obj.expires_at - datetime.now(timezone.utc)).days
                if old_key_obj.expires_at else None
            ),
            metadata=old_key_obj.metadata
        )
        
        # Revoke old key
        await self.revoke_api_key(key_id, user_email)
        
        logger.info(f"Rotated API key {key_id} for {user_email}")
        
        return new_key, plain_key
    
    async def update_api_key(
        self,
        key_id: str,
        user_email: str,
        name: str = None,
        scopes: List[str] = None,
        metadata: Dict[str, Any] = None
    ) -> bool:
        """Update API key properties (not the key itself)"""
        update_data = {'updated_at': datetime.now(timezone.utc)}
        
        if name:
            update_data['name'] = name
        
        if scopes is not None:
            invalid_scopes = [s for s in scopes if s not in self.AVAILABLE_SCOPES]
            if invalid_scopes:
                raise ValueError(f"Invalid scopes: {invalid_scopes}")
            update_data['scopes'] = scopes
        
        if metadata is not None:
            update_data['metadata'] = metadata
        
        result = await self.collection.update_one(
            {'id': key_id, 'user_email': user_email},
            {'$set': update_data}
        )
        
        return result.modified_count > 0
    
    async def get_key_usage_stats(self, key_id: str, user_email: str) -> Dict:
        """Get usage statistics for an API key"""
        key_data = await self.collection.find_one({
            'id': key_id,
            'user_email': user_email
        })
        
        if not key_data:
            return None
        
        api_key = APIKey(**key_data)
        
        return {
            'id': api_key.id,
            'name': api_key.name,
            'key_prefix': api_key.key_prefix,
            'usage_count': api_key.usage_count,
            'last_used_at': api_key.last_used_at,
            'created_at': api_key.created_at,
            'is_active': api_key.is_active,
            'expires_at': api_key.expires_at,
            'scopes': api_key.scopes
        }
    
    async def cleanup_expired_keys(self) -> int:
        """Remove expired keys (runs periodically)"""
        result = await self.collection.update_many(
            {
                'expires_at': {'$lt': datetime.now(timezone.utc)},
                'is_active': True
            },
            {'$set': {'is_active': False}}
        )
        
        if result.modified_count > 0:
            logger.info(f"Deactivated {result.modified_count} expired API keys")
        
        return result.modified_count


# Dependency for FastAPI routes
async def get_api_key_from_header(
    request,
    api_key_manager: APIKeyManager,
    required_scopes: List[str] = None
) -> Optional[APIKey]:
    """
    FastAPI dependency to extract and validate API key from header
    Usage: api_key: APIKey = Depends(get_api_key_from_header)
    """
    from fastapi import HTTPException
    
    # Check for API key in header
    api_key = request.headers.get("X-API-Key")
    
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key required",
            headers={"WWW-Authenticate": "ApiKey"}
        )
    
    # Validate key
    validated_key = await api_key_manager.validate_api_key(api_key, required_scopes)
    
    if not validated_key:
        raise HTTPException(
            status_code=403,
            detail="Invalid or insufficient API key permissions"
        )
    
    return validated_key
