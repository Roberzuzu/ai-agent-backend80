"""
Security Headers Middleware
Implements security headers similar to Helmet.js
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from typing import Callable
import logging

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add security headers to all responses
    Equivalent to Helmet.js for FastAPI
    """
    
    def __init__(self, app, config: dict = None):
        super().__init__(app)
        self.config = config or {}
        
        # Default security headers
        self.default_headers = {
            # Prevent clickjacking
            "X-Frame-Options": "DENY",
            
            # Prevent MIME type sniffing
            "X-Content-Type-Options": "nosniff",
            
            # Enable XSS protection
            "X-XSS-Protection": "1; mode=block",
            
            # Referrer policy
            "Referrer-Policy": "strict-origin-when-cross-origin",
            
            # Permissions policy
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
            
            # HSTS (HTTP Strict Transport Security)
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            
            # Content Security Policy
            "Content-Security-Policy": self._get_csp_header(),
        }
        
        # Merge with custom config
        self.headers = {**self.default_headers, **self.config.get('headers', {})}
    
    def _get_csp_header(self) -> str:
        """
        Build Content Security Policy header
        Customize based on your app needs
        """
        directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "font-src 'self' https://fonts.gstatic.com data:",
            "img-src 'self' data: https: blob:",
            "connect-src 'self' https://api.stripe.com https://checkout.stripe.com",
            "frame-src 'self' https://js.stripe.com https://hooks.stripe.com",
            "object-src 'none'",
            "base-uri 'self'",
            "form-action 'self'",
            "frame-ancestors 'none'",
            "upgrade-insecure-requests"
        ]
        
        return "; ".join(directives)
    
    async def dispatch(self, request: Request, call_next: Callable):
        """Add security headers to response"""
        response = await call_next(request)
        
        # Add all security headers
        for header, value in self.headers.items():
            response.headers[header] = value
        
        # Add custom headers for development
        if self.config.get('development', False):
            response.headers["X-Powered-By"] = "FastAPI"
        else:
            # Remove X-Powered-By in production
            if "X-Powered-By" in response.headers:
                del response.headers["X-Powered-By"]
        
        return response


def configure_cors_security(app, allowed_origins: list = None):
    """
    Configure secure CORS settings
    More restrictive than default CORSMiddleware
    """
    from starlette.middleware.cors import CORSMiddleware
    
    if allowed_origins is None:
        allowed_origins = [
            "http://localhost:3000",
            "https://localhost:3000",
        ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=[
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "X-CSRF-Token",
            "X-API-Key"
        ],
        expose_headers=[
            "X-RateLimit-Limit",
            "X-RateLimit-Remaining",
            "X-RateLimit-Reset",
            "Retry-After"
        ],
        max_age=3600
    )


class IPWhitelistMiddleware(BaseHTTPMiddleware):
    """
    Restrict admin endpoints to whitelisted IPs
    """
    
    def __init__(self, app, whitelist: list = None, admin_paths: list = None):
        super().__init__(app)
        self.whitelist = set(whitelist or [])
        self.admin_paths = admin_paths or [
            "/api/admin",
            "/api/database",
            "/api/audit-logs"
        ]
    
    async def dispatch(self, request: Request, call_next: Callable):
        """Check IP whitelist for admin endpoints"""
        from fastapi.responses import JSONResponse
        
        # Get client IP
        client_ip = request.client.host
        
        # Check if request is for admin endpoint
        path = request.url.path
        is_admin_path = any(path.startswith(admin_path) for admin_path in self.admin_paths)
        
        if is_admin_path and self.whitelist:
            if client_ip not in self.whitelist:
                logger.warning(f"Blocked admin access from non-whitelisted IP: {client_ip}")
                return JSONResponse(
                    status_code=403,
                    content={
                        "error": "Forbidden",
                        "detail": "Access to admin endpoints is restricted to whitelisted IPs"
                    }
                )
        
        return await call_next(request)
    
    def add_ip(self, ip: str):
        """Add IP to whitelist"""
        self.whitelist.add(ip)
        logger.info(f"Added IP to admin whitelist: {ip}")
    
    def remove_ip(self, ip: str):
        """Remove IP from whitelist"""
        self.whitelist.discard(ip)
        logger.info(f"Removed IP from admin whitelist: {ip}")


class CSRFProtectionMiddleware(BaseHTTPMiddleware):
    """
    CSRF Protection for state-changing operations
    """
    
    def __init__(self, app, exempt_paths: list = None):
        super().__init__(app)
        self.exempt_paths = set(exempt_paths or [
            "/api/auth/login",
            "/api/auth/register",
            "/api/webhook"
        ])
    
    async def dispatch(self, request: Request, call_next: Callable):
        """Verify CSRF token for unsafe methods"""
        from fastapi.responses import JSONResponse
        
        # Only check for state-changing methods
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            path = request.url.path
            
            # Skip exempt paths
            if not any(path.startswith(exempt) for exempt in self.exempt_paths):
                # Check for CSRF token in header
                csrf_token = request.headers.get("X-CSRF-Token")
                
                # For now, just log - in production, validate against session
                if not csrf_token:
                    logger.warning(f"Missing CSRF token for {request.method} {path}")
                    # In production, return 403:
                    # return JSONResponse(
                    #     status_code=403,
                    #     content={"error": "CSRF token missing"}
                    # )
        
        return await call_next(request)
