"""
Structured Logging System
JSON logging with rotation and filtering
"""
import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import traceback


class JSONFormatter(logging.Formatter):
    """Format logs as JSON for easier parsing"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }
        
        # Add extra fields
        if hasattr(record, 'extra'):
            log_data['extra'] = record.extra
        
        # Add request context if available
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        
        if hasattr(record, 'user_email'):
            log_data['user_email'] = record.user_email
        
        if hasattr(record, 'ip_address'):
            log_data['ip_address'] = record.ip_address
        
        return json.dumps(log_data)


class ContextFilter(logging.Filter):
    """Add context information to log records"""
    
    def __init__(self):
        super().__init__()
        self.request_context = {}
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Add context to record"""
        # Add request context if available
        for key, value in self.request_context.items():
            setattr(record, key, value)
        
        return True
    
    def set_context(self, **kwargs):
        """Set context for subsequent log records"""
        self.request_context.update(kwargs)
    
    def clear_context(self):
        """Clear request context"""
        self.request_context.clear()


def setup_logging(
    log_level: str = 'INFO',
    log_file: str = '/var/log/app/backend.log',
    json_logging: bool = True,
    enable_rotation: bool = True
):
    """
    Setup comprehensive logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
        json_logging: Use JSON format for logs
        enable_rotation: Enable log rotation
    """
    # Create logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Console handler (always human-readable)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler with rotation
    if enable_rotation:
        # Rotate daily, keep 30 days
        file_handler = TimedRotatingFileHandler(
            log_file,
            when='midnight',
            interval=1,
            backupCount=30,
            encoding='utf-8'
        )
    else:
        # Simple rotating file handler (10MB, 5 backups)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
    
    file_handler.setLevel(logging.DEBUG)
    
    if json_logging:
        file_handler.setFormatter(JSONFormatter())
    else:
        file_handler.setFormatter(console_formatter)
    
    root_logger.addHandler(file_handler)
    
    # Error file handler (only errors and critical)
    error_file = log_file.replace('.log', '.error.log')
    error_handler = RotatingFileHandler(
        error_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=10,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(JSONFormatter() if json_logging else console_formatter)
    root_logger.addHandler(error_handler)
    
    # Add context filter
    context_filter = ContextFilter()
    root_logger.addFilter(context_filter)
    
    logging.info(f"Logging configured: level={log_level}, json={json_logging}, rotation={enable_rotation}")
    
    return context_filter


# Logging middleware for FastAPI
class LoggingMiddleware:
    """Middleware to log all requests"""
    
    def __init__(self, app, logger_name: str = "api"):
        self.app = app
        self.logger = logging.getLogger(logger_name)
    
    async def __call__(self, scope, receive, send):
        """Log requests and responses"""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        start_time = datetime.now()
        
        # Extract request info
        method = scope["method"]
        path = scope["path"]
        client = scope.get("client", ("unknown", 0))
        ip_address = client[0] if client else "unknown"
        
        # Generate request ID
        import uuid
        request_id = str(uuid.uuid4())
        
        # Log request
        self.logger.info(
            f"Request: {method} {path}",
            extra={
                'request_id': request_id,
                'method': method,
                'path': path,
                'ip_address': ip_address,
                'event': 'request_start'
            }
        )
        
        # Process request
        status_code = 500
        
        async def send_wrapper(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)
        
        try:
            await self.app(scope, receive, send_wrapper)
        except Exception as e:
            self.logger.error(
                f"Request error: {method} {path}",
                exc_info=True,
                extra={
                    'request_id': request_id,
                    'method': method,
                    'path': path,
                    'ip_address': ip_address,
                    'event': 'request_error'
                }
            )
            raise
        finally:
            # Log response
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            log_level = logging.INFO
            if status_code >= 500:
                log_level = logging.ERROR
            elif status_code >= 400:
                log_level = logging.WARNING
            
            self.logger.log(
                log_level,
                f"Response: {method} {path} - {status_code} ({duration_ms:.2f}ms)",
                extra={
                    'request_id': request_id,
                    'method': method,
                    'path': path,
                    'ip_address': ip_address,
                    'status_code': status_code,
                    'duration_ms': round(duration_ms, 2),
                    'event': 'request_complete'
                }
            )


# Helper functions
def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(name)


def log_with_context(logger: logging.Logger, level: str, message: str, **context):
    """Log message with additional context"""
    log_method = getattr(logger, level.lower())
    log_method(message, extra=context)
