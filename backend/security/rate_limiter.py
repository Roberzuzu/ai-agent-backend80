"""
Rate Limiting System
Advanced rate limiting with sliding window algorithm
Supports per-IP, per-endpoint, and role-based limits
"""
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Advanced rate limiter with sliding window algorithm
    Memory-based (no Redis required)
    """
    
    def __init__(self):
        # Store: {identifier: [(timestamp, weight), ...]}
        self.requests: Dict[str, list] = defaultdict(list)
        self.lock = asyncio.Lock()
        
        # Default limits (requests per window)
        self.default_limits = {
            'per_minute': 60,
            'per_hour': 1000,
            'per_day': 10000
        }
        
        # Role-based multipliers
        self.role_multipliers = {
            'user': 1.0,
            'admin': 10.0,
            'affiliate': 2.0
        }
        
        # Endpoint-specific limits (overrides defaults)
        self.endpoint_limits = {
            '/api/auth/login': {'per_minute': 5, 'per_hour': 20},
            '/api/auth/register': {'per_minute': 3, 'per_hour': 10},
            '/api/payments/checkout/session': {'per_minute': 10, 'per_hour': 100},
            '/api/ai/generate': {'per_minute': 5, 'per_hour': 50},
            '/api/database/backup': {'per_hour': 5, 'per_day': 20},
        }
        
        # Trusted IPs (bypass rate limiting)
        self.trusted_ips = set()
    
    def add_trusted_ip(self, ip: str):
        """Add IP to trusted list (bypasses rate limiting)"""
        self.trusted_ips.add(ip)
        logger.info(f"Added trusted IP: {ip}")
    
    def remove_trusted_ip(self, ip: str):
        """Remove IP from trusted list"""
        self.trusted_ips.discard(ip)
        logger.info(f"Removed trusted IP: {ip}")
    
    async def check_rate_limit(
        self,
        identifier: str,
        endpoint: str = "default",
        role: str = "user"
    ) -> Tuple[bool, Dict[str, any]]:
        """
        Check if request is allowed
        
        Args:
            identifier: IP address or user ID
            endpoint: API endpoint path
            role: User role (user, admin, affiliate)
        
        Returns:
            (allowed: bool, info: dict)
        """
        # Bypass for trusted IPs
        if identifier in self.trusted_ips:
            return True, {'trusted': True}
        
        async with self.lock:
            now = datetime.now()
            
            # Get limits for this endpoint
            limits = self.endpoint_limits.get(endpoint, self.default_limits)
            
            # Apply role multiplier
            multiplier = self.role_multipliers.get(role, 1.0)
            effective_limits = {
                k: int(v * multiplier) for k, v in limits.items()
            }
            
            # Clean old requests
            self._cleanup_old_requests(identifier, now)
            
            # Check each window
            windows = {
                'per_minute': timedelta(minutes=1),
                'per_hour': timedelta(hours=1),
                'per_day': timedelta(days=1)
            }
            
            for window_name, window_delta in windows.items():
                if window_name not in effective_limits:
                    continue
                
                limit = effective_limits[window_name]
                count = self._count_requests(identifier, now, window_delta)
                
                if count >= limit:
                    retry_after = self._calculate_retry_after(
                        identifier, now, window_delta, limit
                    )
                    return False, {
                        'window': window_name,
                        'limit': limit,
                        'current': count,
                        'retry_after': retry_after
                    }
            
            # Add current request
            self.requests[identifier].append((now, 1))
            
            # Get current usage stats
            stats = {
                'per_minute': self._count_requests(identifier, now, timedelta(minutes=1)),
                'per_hour': self._count_requests(identifier, now, timedelta(hours=1)),
                'per_day': self._count_requests(identifier, now, timedelta(days=1)),
            }
            
            return True, {
                'allowed': True,
                'limits': effective_limits,
                'current': stats
            }
    
    def _cleanup_old_requests(self, identifier: str, now: datetime):
        """Remove requests older than 24 hours"""
        if identifier not in self.requests:
            return
        
        cutoff = now - timedelta(days=1)
        self.requests[identifier] = [
            (ts, weight) for ts, weight in self.requests[identifier]
            if ts > cutoff
        ]
        
        # Remove empty entries
        if not self.requests[identifier]:
            del self.requests[identifier]
    
    def _count_requests(
        self,
        identifier: str,
        now: datetime,
        window: timedelta
    ) -> int:
        """Count requests in a time window"""
        if identifier not in self.requests:
            return 0
        
        cutoff = now - window
        return sum(
            weight for ts, weight in self.requests[identifier]
            if ts > cutoff
        )
    
    def _calculate_retry_after(
        self,
        identifier: str,
        now: datetime,
        window: timedelta,
        limit: int
    ) -> int:
        """Calculate seconds until rate limit resets"""
        if identifier not in self.requests:
            return 0
        
        cutoff = now - window
        requests_in_window = [
            ts for ts, _ in self.requests[identifier]
            if ts > cutoff
        ]
        
        if not requests_in_window or len(requests_in_window) < limit:
            return 0
        
        # Find the oldest request that will age out
        oldest_request = min(requests_in_window)
        retry_time = oldest_request + window
        return max(0, int((retry_time - now).total_seconds()))
    
    async def reset_identifier(self, identifier: str):
        """Reset rate limit for an identifier"""
        async with self.lock:
            if identifier in self.requests:
                del self.requests[identifier]
                logger.info(f"Reset rate limit for: {identifier}")
    
    def get_stats(self) -> Dict:
        """Get rate limiter statistics"""
        return {
            'total_identifiers': len(self.requests),
            'trusted_ips': len(self.trusted_ips),
            'total_requests': sum(len(reqs) for reqs in self.requests.values())
        }


# Global rate limiter instance
rate_limiter = RateLimiter()


# Middleware function for FastAPI
async def rate_limit_middleware(
    request,
    call_next,
    rate_limiter: RateLimiter,
    get_user_role=None
):
    """
    FastAPI middleware for rate limiting
    
    Args:
        request: FastAPI request
        call_next: Next middleware/endpoint
        rate_limiter: RateLimiter instance
        get_user_role: Optional function to extract user role from request
    """
    from fastapi import HTTPException
    from fastapi.responses import JSONResponse
    
    # Get client IP
    client_ip = request.client.host
    
    # Get endpoint
    endpoint = request.url.path
    
    # Get user role (if authenticated)
    role = "user"
    if get_user_role:
        try:
            role = await get_user_role(request)
        except:
            pass
    
    # Check rate limit
    allowed, info = await rate_limiter.check_rate_limit(
        identifier=client_ip,
        endpoint=endpoint,
        role=role
    )
    
    if not allowed:
        return JSONResponse(
            status_code=429,
            content={
                "error": "Rate limit exceeded",
                "detail": f"Too many requests. Try again in {info['retry_after']} seconds.",
                "window": info['window'],
                "limit": info['limit'],
                "current": info['current'],
                "retry_after": info['retry_after']
            },
            headers={
                "Retry-After": str(info['retry_after']),
                "X-RateLimit-Limit": str(info['limit']),
                "X-RateLimit-Remaining": str(max(0, info['limit'] - info['current'])),
                "X-RateLimit-Reset": str(info['retry_after'])
            }
        )
    
    # Add rate limit headers to response
    response = await call_next(request)
    
    if 'limits' in info and 'current' in info:
        # Use per_minute as primary limit for headers
        limit = info['limits'].get('per_minute', 60)
        current = info['current'].get('per_minute', 0)
        
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(max(0, limit - current))
    
    return response
