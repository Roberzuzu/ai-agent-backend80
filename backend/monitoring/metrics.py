"""
Application Metrics and Monitoring
Prometheus-compatible metrics exporter
"""
from typing import Dict, Any, List
from collections import defaultdict
from datetime import datetime, timezone, timedelta
import time
import asyncio
import psutil


class MetricsCollector:
    """Collect and expose application metrics"""
    
    def __init__(self):
        # Request metrics
        self.request_count = defaultdict(int)
        self.request_duration = defaultdict(list)
        self.error_count = defaultdict(int)
        
        # Custom business metrics
        self.custom_metrics = {}
        
        # System metrics cache
        self.last_system_check = None
        self.system_metrics_cache = {}
    
    def record_request(self, method: str, endpoint: str, status_code: int, duration_ms: float):
        """Record HTTP request metrics"""
        key = f"{method}:{endpoint}"
        self.request_count[key] += 1
        self.request_duration[key].append(duration_ms)
        
        if status_code >= 400:
            self.error_count[key] += 1
    
    def set_custom_metric(self, name: str, value: float, labels: Dict[str, str] = None):
        """Set a custom metric value"""
        key = name
        if labels:
            label_str = ','.join(f'{k}="{v}"' for k, v in labels.items())
            key = f"{name}{{{label_str}}}"
        
        self.custom_metrics[key] = {
            'value': value,
            'timestamp': time.time()
        }
    
    def increment_counter(self, name: str, amount: int = 1, labels: Dict[str, str] = None):
        """Increment a counter metric"""
        key = name
        if labels:
            label_str = ','.join(f'{k}="{v}"' for k, v in labels.items())
            key = f"{name}{{{label_str}}}"
        
        if key not in self.custom_metrics:
            self.custom_metrics[key] = {'value': 0, 'timestamp': time.time()}
        
        self.custom_metrics[key]['value'] += amount
        self.custom_metrics[key]['timestamp'] = time.time()
    
    def get_request_metrics(self) -> Dict[str, Any]:
        """Get aggregated request metrics"""
        metrics = {}
        
        for endpoint, count in self.request_count.items():
            durations = self.request_duration[endpoint]
            errors = self.error_count[endpoint]
            
            metrics[endpoint] = {
                'total_requests': count,
                'error_count': errors,
                'error_rate': round((errors / count) * 100, 2) if count > 0 else 0,
                'avg_duration_ms': round(sum(durations) / len(durations), 2) if durations else 0,
                'min_duration_ms': round(min(durations), 2) if durations else 0,
                'max_duration_ms': round(max(durations), 2) if durations else 0,
                'p95_duration_ms': self._calculate_percentile(durations, 95) if durations else 0,
                'p99_duration_ms': self._calculate_percentile(durations, 99) if durations else 0
            }
        
        return metrics
    
    def get_system_metrics(self, cache_seconds: int = 5) -> Dict[str, Any]:
        """Get system metrics (cached)"""
        now = time.time()
        
        # Return cached if recent
        if (self.last_system_check and 
            now - self.last_system_check < cache_seconds and
            self.system_metrics_cache):
            return self.system_metrics_cache
        
        # Collect fresh metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_count = psutil.cpu_count()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Network I/O
        net_io = psutil.net_io_counters()
        
        metrics = {
            'cpu': {
                'percent': round(cpu_percent, 2),
                'count': cpu_count,
                'per_cpu': [round(p, 2) for p in psutil.cpu_percent(interval=0.1, percpu=True)]
            },
            'memory': {
                'total_bytes': memory.total,
                'available_bytes': memory.available,
                'used_bytes': memory.used,
                'percent': round(memory.percent, 2)
            },
            'disk': {
                'total_bytes': disk.total,
                'used_bytes': disk.used,
                'free_bytes': disk.free,
                'percent': round(disk.percent, 2)
            },
            'network': {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv
            }
        }
        
        self.system_metrics_cache = metrics
        self.last_system_check = now
        
        return metrics
    
    def get_custom_metrics(self) -> Dict[str, Any]:
        """Get all custom metrics"""
        return self.custom_metrics.copy()
    
    def export_prometheus_format(self) -> str:
        """Export metrics in Prometheus text format"""
        lines = []
        
        # Request metrics
        for endpoint, metrics in self.get_request_metrics().items():
            method, path = endpoint.split(':', 1)
            labels = f'method="{method}",endpoint="{path}"'
            
            lines.append(f'# HELP http_requests_total Total HTTP requests')
            lines.append(f'# TYPE http_requests_total counter')
            lines.append(f'http_requests_total{{{labels}}} {metrics["total_requests"]}')
            
            lines.append(f'# HELP http_request_duration_milliseconds HTTP request duration')
            lines.append(f'# TYPE http_request_duration_milliseconds summary')
            lines.append(f'http_request_duration_milliseconds{{quantile="0.5",{labels}}} {metrics["avg_duration_ms"]}')
            lines.append(f'http_request_duration_milliseconds{{quantile="0.95",{labels}}} {metrics["p95_duration_ms"]}')
            lines.append(f'http_request_duration_milliseconds{{quantile="0.99",{labels}}} {metrics["p99_duration_ms"]}')
            
            lines.append(f'# HELP http_errors_total Total HTTP errors')
            lines.append(f'# TYPE http_errors_total counter')
            lines.append(f'http_errors_total{{{labels}}} {metrics["error_count"]}')
        
        # System metrics
        system = self.get_system_metrics()
        
        lines.append(f'# HELP system_cpu_percent CPU usage percentage')
        lines.append(f'# TYPE system_cpu_percent gauge')
        lines.append(f'system_cpu_percent {system["cpu"]["percent"]}')
        
        lines.append(f'# HELP system_memory_used_bytes Memory used in bytes')
        lines.append(f'# TYPE system_memory_used_bytes gauge')
        lines.append(f'system_memory_used_bytes {system["memory"]["used_bytes"]}')
        
        lines.append(f'# HELP system_disk_used_bytes Disk used in bytes')
        lines.append(f'# TYPE system_disk_used_bytes gauge')
        lines.append(f'system_disk_used_bytes {system["disk"]["used_bytes"]}')
        
        # Custom metrics
        for name, data in self.custom_metrics.items():
            lines.append(f'# HELP {name} Custom metric')
            lines.append(f'# TYPE {name} gauge')
            lines.append(f'{name} {data["value"]}')
        
        return '\n'.join(lines) + '\n'
    
    @staticmethod
    def _calculate_percentile(values: List[float], percentile: int) -> float:
        """Calculate percentile value"""
        if not values:
            return 0
        
        sorted_values = sorted(values)
        index = int((percentile / 100) * len(sorted_values))
        index = min(index, len(sorted_values) - 1)
        
        return round(sorted_values[index], 2)
    
    def reset_metrics(self):
        """Reset all metrics (useful for testing)"""
        self.request_count.clear()
        self.request_duration.clear()
        self.error_count.clear()
        self.custom_metrics.clear()


# Global metrics collector
metrics_collector = MetricsCollector()


# Monitoring middleware
class MetricsMiddleware:
    """Middleware to collect request metrics"""
    
    def __init__(self, app, metrics_collector: MetricsCollector):
        self.app = app
        self.metrics = metrics_collector
    
    async def __call__(self, scope, receive, send):
        """Collect metrics for each request"""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        start_time = time.time()
        method = scope["method"]
        path = scope["path"]
        status_code = 500
        
        async def send_wrapper(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)
        
        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            duration_ms = (time.time() - start_time) * 1000
            self.metrics.record_request(method, path, status_code, duration_ms)


# Helper function for business metrics
async def track_business_metric(
    metrics_collector: MetricsCollector,
    metric_name: str,
    value: float,
    labels: Dict[str, str] = None
):
    """Track a business metric"""
    metrics_collector.set_custom_metric(metric_name, value, labels)
