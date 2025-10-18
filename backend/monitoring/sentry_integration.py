"""
Sentry Error Tracking Integration
Captures and reports errors to Sentry
"""
import logging
import os
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class SentryIntegration:
    """Sentry error tracking integration"""
    
    def __init__(self, dsn: Optional[str] = None, environment: str = "development"):
        self.dsn = dsn or os.environ.get('SENTRY_DSN')
        self.environment = environment
        self.enabled = False
        self.sentry = None
        
        if self.dsn:
            self._initialize_sentry()
        else:
            logger.warning("Sentry DSN not configured - error tracking disabled")
    
    def _initialize_sentry(self):
        """Initialize Sentry SDK"""
        try:
            import sentry_sdk
            from sentry_sdk.integrations.fastapi import FastApiIntegration
            from sentry_sdk.integrations.logging import LoggingIntegration
            
            # Configure Sentry
            sentry_sdk.init(
                dsn=self.dsn,
                environment=self.environment,
                
                # Integrations
                integrations=[
                    FastApiIntegration(
                        transaction_style="endpoint"
                    ),
                    LoggingIntegration(
                        level=logging.INFO,  # Capture info and above as breadcrumbs
                        event_level=logging.ERROR  # Send errors as events
                    ),
                ],
                
                # Performance monitoring
                traces_sample_rate=0.1,  # 10% of transactions
                
                # Error sampling
                sample_rate=1.0,  # 100% of errors
                
                # Release tracking
                release=os.environ.get('APP_VERSION', 'unknown'),
                
                # Additional options
                attach_stacktrace=True,
                send_default_pii=False,  # Don't send PII
                max_breadcrumbs=50,
            )
            
            self.sentry = sentry_sdk
            self.enabled = True
            logger.info(f"Sentry initialized for environment: {self.environment}")
            
        except ImportError:
            logger.error("sentry-sdk not installed. Install with: pip install sentry-sdk")
        except Exception as e:
            logger.error(f"Failed to initialize Sentry: {e}")
    
    def capture_exception(self, error: Exception, context: Dict[str, Any] = None):
        """Capture an exception and send to Sentry"""
        if not self.enabled:
            return
        
        try:
            if context:
                with self.sentry.configure_scope() as scope:
                    for key, value in context.items():
                        scope.set_context(key, value)
            
            self.sentry.capture_exception(error)
        except Exception as e:
            logger.error(f"Failed to capture exception in Sentry: {e}")
    
    def capture_message(self, message: str, level: str = "info", context: Dict[str, Any] = None):
        """Capture a message and send to Sentry"""
        if not self.enabled:
            return
        
        try:
            if context:
                with self.sentry.configure_scope() as scope:
                    for key, value in context.items():
                        scope.set_context(key, value)
            
            self.sentry.capture_message(message, level=level)
        except Exception as e:
            logger.error(f"Failed to capture message in Sentry: {e}")
    
    def set_user(self, user_id: str, email: str = None, username: str = None):
        """Set user context for error tracking"""
        if not self.enabled:
            return
        
        try:
            with self.sentry.configure_scope() as scope:
                scope.set_user({
                    "id": user_id,
                    "email": email,
                    "username": username
                })
        except Exception as e:
            logger.error(f"Failed to set user context: {e}")
    
    def add_breadcrumb(self, message: str, category: str = "default", level: str = "info", data: Dict = None):
        """Add a breadcrumb for context"""
        if not self.enabled:
            return
        
        try:
            self.sentry.add_breadcrumb({
                "message": message,
                "category": category,
                "level": level,
                "data": data or {}
            })
        except Exception as e:
            logger.error(f"Failed to add breadcrumb: {e}")
    
    def start_transaction(self, name: str, op: str = "default"):
        """Start a performance transaction"""
        if not self.enabled:
            return None
        
        try:
            return self.sentry.start_transaction(name=name, op=op)
        except Exception as e:
            logger.error(f"Failed to start transaction: {e}")
            return None


# Global Sentry instance
sentry_integration = None


def initialize_sentry(dsn: Optional[str] = None, environment: str = "development"):
    """Initialize global Sentry instance"""
    global sentry_integration
    sentry_integration = SentryIntegration(dsn=dsn, environment=environment)
    return sentry_integration


def get_sentry() -> SentryIntegration:
    """Get global Sentry instance"""
    global sentry_integration
    if sentry_integration is None:
        sentry_integration = SentryIntegration()
    return sentry_integration


# Middleware for FastAPI
class SentryMiddleware:
    """Middleware to capture errors in Sentry"""
    
    def __init__(self, app, sentry: SentryIntegration):
        self.app = app
        self.sentry = sentry
    
    async def __call__(self, scope, receive, send):
        """Capture errors and send to Sentry"""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        try:
            # Add breadcrumb for request
            self.sentry.add_breadcrumb(
                message=f"{scope['method']} {scope['path']}",
                category="request",
                data={
                    "method": scope["method"],
                    "path": scope["path"],
                    "query_string": scope.get("query_string", b"").decode()
                }
            )
            
            await self.app(scope, receive, send)
            
        except Exception as e:
            # Capture exception with context
            self.sentry.capture_exception(e, context={
                "request": {
                    "method": scope["method"],
                    "path": scope["path"],
                    "headers": dict(scope.get("headers", []))
                }
            })
            raise


# Usage example in .env file:
"""
# Add to .env:
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
APP_VERSION=1.0.0
ENVIRONMENT=production
"""

# Usage example in code:
"""
# Initialize Sentry
from monitoring.sentry_integration import initialize_sentry
sentry = initialize_sentry(
    dsn=os.environ.get('SENTRY_DSN'),
    environment=os.environ.get('ENVIRONMENT', 'development')
)

# Capture exception
try:
    risky_operation()
except Exception as e:
    sentry.capture_exception(e, context={'user_id': user_id})

# Capture message
sentry.capture_message("Important event occurred", level="warning")

# Add breadcrumb
sentry.add_breadcrumb("User clicked checkout", category="user_action")

# Set user context
sentry.set_user(user_id="123", email="user@example.com")
"""
