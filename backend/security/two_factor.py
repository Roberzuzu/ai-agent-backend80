"""
Two-Factor Authentication (2FA) System
TOTP-based 2FA with QR code generation
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorDatabase
import pyotp
import qrcode
from io import BytesIO
import base64
import secrets
import logging

logger = logging.getLogger(__name__)


class TwoFactorAuth(BaseModel):
    """2FA configuration model"""
    user_email: str
    secret: str  # TOTP secret
    is_enabled: bool = False
    backup_codes: List[str] = []  # Recovery codes
    last_used_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TwoFactorSetup(BaseModel):
    """2FA setup response"""
    secret: str
    qr_code: str  # Base64 encoded QR code image
    backup_codes: List[str]
    manual_entry_key: str  # For manual entry in authenticator apps


class TwoFactorManager:
    """Manage 2FA setup, verification, and recovery"""
    
    def __init__(self, db: AsyncIOMotorDatabase, app_name: str = "Emergent App"):
        self.db = db
        self.collection = db['two_factor_auth']
        self.app_name = app_name
    
    @staticmethod
    def generate_secret() -> str:
        """Generate a new TOTP secret"""
        return pyotp.random_base32()
    
    @staticmethod
    def generate_backup_codes(count: int = 10) -> List[str]:
        """Generate backup recovery codes"""
        return [
            f"{secrets.token_hex(4)}-{secrets.token_hex(4)}"
            for _ in range(count)
        ]
    
    def generate_qr_code(self, secret: str, user_email: str) -> str:
        """
        Generate QR code for TOTP setup
        Returns base64-encoded PNG image
        """
        # Create provisioning URI
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(
            name=user_email,
            issuer_name=self.app_name
        )
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    async def setup_2fa(self, user_email: str) -> TwoFactorSetup:
        """
        Initialize 2FA setup for a user
        Returns secret, QR code, and backup codes
        """
        # Check if 2FA already exists
        existing = await self.collection.find_one({'user_email': user_email})
        
        if existing and existing.get('is_enabled'):
            raise ValueError("2FA is already enabled for this user")
        
        # Generate secret and backup codes
        secret = self.generate_secret()
        backup_codes = self.generate_backup_codes()
        
        # Generate QR code
        qr_code = self.generate_qr_code(secret, user_email)
        
        # Save to database (not enabled yet)
        two_factor_config = TwoFactorAuth(
            user_email=user_email,
            secret=secret,
            is_enabled=False,
            backup_codes=backup_codes
        )
        
        await self.collection.update_one(
            {'user_email': user_email},
            {'$set': two_factor_config.model_dump()},
            upsert=True
        )
        
        logger.info(f"2FA setup initiated for {user_email}")
        
        # Return setup info
        return TwoFactorSetup(
            secret=secret,
            qr_code=qr_code,
            backup_codes=backup_codes,
            manual_entry_key=secret  # For manual entry
        )
    
    async def enable_2fa(self, user_email: str, verification_code: str) -> bool:
        """
        Enable 2FA after verifying the first code
        """
        # Get 2FA config
        config = await self.collection.find_one({'user_email': user_email})
        
        if not config:
            raise ValueError("2FA not setup for this user")
        
        if config.get('is_enabled'):
            raise ValueError("2FA already enabled")
        
        # Verify code
        if not self.verify_code(config['secret'], verification_code):
            return False
        
        # Enable 2FA
        await self.collection.update_one(
            {'user_email': user_email},
            {
                '$set': {
                    'is_enabled': True,
                    'updated_at': datetime.now(timezone.utc)
                }
            }
        )
        
        logger.info(f"2FA enabled for {user_email}")
        return True
    
    async def disable_2fa(self, user_email: str, verification_code: str = None) -> bool:
        """
        Disable 2FA (requires verification)
        """
        config = await self.collection.find_one({'user_email': user_email})
        
        if not config or not config.get('is_enabled'):
            return False
        
        # Verify code if provided
        if verification_code:
            is_valid = (
                self.verify_code(config['secret'], verification_code) or
                await self.verify_backup_code(user_email, verification_code)
            )
            if not is_valid:
                return False
        
        # Disable 2FA
        await self.collection.delete_one({'user_email': user_email})
        
        logger.info(f"2FA disabled for {user_email}")
        return True
    
    @staticmethod
    def verify_code(secret: str, code: str) -> bool:
        """
        Verify a TOTP code
        """
        try:
            totp = pyotp.TOTP(secret)
            # Allow 1 time step before and after for clock drift
            return totp.verify(code, valid_window=1)
        except Exception as e:
            logger.error(f"2FA verification error: {e}")
            return False
    
    async def verify_backup_code(self, user_email: str, backup_code: str) -> bool:
        """
        Verify and consume a backup code
        """
        config = await self.collection.find_one({'user_email': user_email})
        
        if not config or not config.get('is_enabled'):
            return False
        
        backup_codes = config.get('backup_codes', [])
        
        if backup_code in backup_codes:
            # Remove used backup code
            backup_codes.remove(backup_code)
            
            await self.collection.update_one(
                {'user_email': user_email},
                {
                    '$set': {
                        'backup_codes': backup_codes,
                        'last_used_at': datetime.now(timezone.utc)
                    }
                }
            )
            
            logger.info(f"Backup code used for {user_email}")
            return True
        
        return False
    
    async def verify_2fa(self, user_email: str, code: str) -> bool:
        """
        Verify 2FA code (TOTP or backup code)
        """
        config = await self.collection.find_one({'user_email': user_email})
        
        if not config or not config.get('is_enabled'):
            return True  # 2FA not enabled, allow access
        
        # Try TOTP first
        if self.verify_code(config['secret'], code):
            # Update last used
            await self.collection.update_one(
                {'user_email': user_email},
                {'$set': {'last_used_at': datetime.now(timezone.utc)}}
            )
            return True
        
        # Try backup code
        return await self.verify_backup_code(user_email, code)
    
    async def is_2fa_enabled(self, user_email: str) -> bool:
        """Check if 2FA is enabled for a user"""
        config = await self.collection.find_one({'user_email': user_email})
        return config.get('is_enabled', False) if config else False
    
    async def regenerate_backup_codes(
        self,
        user_email: str,
        verification_code: str
    ) -> Optional[List[str]]:
        """
        Regenerate backup codes (requires verification)
        """
        config = await self.collection.find_one({'user_email': user_email})
        
        if not config or not config.get('is_enabled'):
            return None
        
        # Verify code
        if not self.verify_code(config['secret'], verification_code):
            return None
        
        # Generate new backup codes
        new_backup_codes = self.generate_backup_codes()
        
        await self.collection.update_one(
            {'user_email': user_email},
            {
                '$set': {
                    'backup_codes': new_backup_codes,
                    'updated_at': datetime.now(timezone.utc)
                }
            }
        )
        
        logger.info(f"Backup codes regenerated for {user_email}")
        return new_backup_codes
    
    async def get_2fa_status(self, user_email: str) -> dict:
        """Get 2FA status for a user"""
        config = await self.collection.find_one({'user_email': user_email})
        
        if not config:
            return {
                'enabled': False,
                'setup_completed': False
            }
        
        return {
            'enabled': config.get('is_enabled', False),
            'setup_completed': True,
            'backup_codes_remaining': len(config.get('backup_codes', [])),
            'last_used_at': config.get('last_used_at'),
            'created_at': config.get('created_at')
        }


# FastAPI dependency for 2FA verification
async def verify_2fa_code(
    request,
    two_factor_manager: TwoFactorManager
):
    """
    Dependency to verify 2FA code from request
    Checks X-2FA-Code header
    """
    from fastapi import HTTPException
    
    # Get user email from request state (assumes authentication middleware)
    if not hasattr(request.state, 'user'):
        return  # Not authenticated, skip 2FA
    
    user_email = request.state.user.email
    
    # Check if 2FA is enabled
    is_enabled = await two_factor_manager.is_2fa_enabled(user_email)
    
    if not is_enabled:
        return  # 2FA not enabled, allow access
    
    # Get 2FA code from header
    two_fa_code = request.headers.get('X-2FA-Code')
    
    if not two_fa_code:
        raise HTTPException(
            status_code=403,
            detail="2FA code required",
            headers={"X-2FA-Required": "true"}
        )
    
    # Verify code
    is_valid = await two_factor_manager.verify_2fa(user_email, two_fa_code)
    
    if not is_valid:
        raise HTTPException(
            status_code=403,
            detail="Invalid 2FA code"
        )
