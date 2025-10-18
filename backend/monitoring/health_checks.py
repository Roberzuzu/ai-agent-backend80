"""
Health Check System
Comprehensive health monitoring for all services
"""
from typing import Dict, Any, Optional
from datetime import datetime, timezone
import asyncio
import time
import psutil
import logging

logger = logging.getLogger(__name__)


class HealthChecker:
    """Comprehensive health check system"""
    
    def __init__(self, db, stripe_enabled: bool = False, openai_enabled: bool = False):
        self.db = db
        self.stripe_enabled = stripe_enabled
        self.openai_enabled = openai_enabled
        self.start_time = time.time()
    
    async def check_database(self) -> Dict[str, Any]:
        """Check MongoDB connectivity and performance"""
        try:
            start = time.time()
            
            # Simple ping
            await self.db.command('ping')
            
            # Get server status
            server_status = await self.db.command('serverStatus')
            
            latency = (time.time() - start) * 1000  # ms
            
            return {
                'status': 'healthy',
                'latency_ms': round(latency, 2),
                'connections': server_status.get('connections', {}).get('current', 0),
                'uptime_seconds': server_status.get('uptime', 0),
                'version': server_status.get('version', 'unknown')
            }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    async def check_stripe(self) -> Dict[str, Any]:
        """Check Stripe API connectivity"""
        if not self.stripe_enabled:
            return {'status': 'disabled'}
        
        try:
            import stripe
            import os
            
            stripe.api_key = os.environ.get('STRIPE_API_KEY')
            
            start = time.time()
            # Try to retrieve account info
            stripe.Account.retrieve()
            latency = (time.time() - start) * 1000
            
            return {
                'status': 'healthy',
                'latency_ms': round(latency, 2)
            }
        except Exception as e:
            logger.error(f"Stripe health check failed: {e}")
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    async def check_openai(self) -> Dict[str, Any]:
        """Check OpenAI API connectivity"""
        if not self.openai_enabled:
            return {'status': 'disabled'}
        
        try:
            from openai import OpenAI
            import os
            
            client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
            
            start = time.time()
            # Simple models list call
            client.models.list()
            latency = (time.time() - start) * 1000
            
            return {
                'status': 'healthy',
                'latency_ms': round(latency, 2)
            }
        except Exception as e:
            logger.error(f"OpenAI health check failed: {e}")
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    def check_system_resources(self) -> Dict[str, Any]:
        """Check system resources (CPU, memory, disk)"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'status': 'healthy',
                'cpu_percent': round(cpu_percent, 2),
                'memory': {
                    'total_mb': round(memory.total / (1024 * 1024), 2),
                    'available_mb': round(memory.available / (1024 * 1024), 2),
                    'percent_used': round(memory.percent, 2)
                },
                'disk': {
                    'total_gb': round(disk.total / (1024 * 1024 * 1024), 2),
                    'free_gb': round(disk.free / (1024 * 1024 * 1024), 2),
                    'percent_used': round(disk.percent, 2)
                }
            }
        except Exception as e:
            logger.error(f"System resources check failed: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    async def check_all(self) -> Dict[str, Any]:
        """Run all health checks"""
        # Run checks in parallel
        db_check, stripe_check, openai_check = await asyncio.gather(
            self.check_database(),
            self.check_stripe(),
            self.check_openai(),
            return_exceptions=True
        )
        
        # System resources (sync)
        system_check = self.check_system_resources()
        
        # Calculate uptime
        uptime_seconds = int(time.time() - self.start_time)
        
        # Determine overall status
        checks = {
            'database': db_check,
            'stripe': stripe_check,
            'openai': openai_check,
            'system': system_check
        }
        
        unhealthy_services = [
            name for name, check in checks.items()
            if isinstance(check, dict) and check.get('status') == 'unhealthy'
        ]
        
        overall_status = 'unhealthy' if unhealthy_services else 'healthy'
        
        return {
            'status': overall_status,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'uptime_seconds': uptime_seconds,
            'checks': checks,
            'unhealthy_services': unhealthy_services
        }
    
    async def liveness_probe(self) -> bool:
        """
        Liveness probe - is the application running?
        Used by Kubernetes/Docker
        """
        try:
            # Just check if we can respond
            return True
        except:
            return False
    
    async def readiness_probe(self) -> bool:
        """
        Readiness probe - is the application ready to serve traffic?
        Checks critical dependencies
        """
        try:
            # Check database connectivity
            db_check = await self.check_database()
            if db_check.get('status') != 'healthy':
                return False
            
            # Check system resources aren't critical
            system_check = self.check_system_resources()
            if system_check.get('status') == 'error':
                return False
            
            # Check memory isn't critically low
            memory_percent = system_check.get('memory', {}).get('percent_used', 0)
            if memory_percent > 95:
                return False
            
            return True
        except:
            return False


# FastAPI endpoints
async def health_check_endpoint(health_checker: HealthChecker):
    """Detailed health check endpoint"""
    result = await health_checker.check_all()
    
    # Return 503 if unhealthy
    status_code = 200 if result['status'] == 'healthy' else 503
    
    return result, status_code


async def liveness_endpoint(health_checker: HealthChecker):
    """Kubernetes liveness probe endpoint"""
    is_alive = await health_checker.liveness_probe()
    
    if is_alive:
        return {'status': 'alive'}, 200
    else:
        return {'status': 'dead'}, 503


async def readiness_endpoint(health_checker: HealthChecker):
    """Kubernetes readiness probe endpoint"""
    is_ready = await health_checker.readiness_probe()
    
    if is_ready:
        return {'status': 'ready'}, 200
    else:
        return {'status': 'not_ready'}, 503
