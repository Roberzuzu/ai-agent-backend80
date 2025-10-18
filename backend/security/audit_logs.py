"""
Audit Logging System
Track critical operations and data changes
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging
import json

logger = logging.getLogger(__name__)


class AuditLog(BaseModel):
    """Audit log entry model"""
    id: str
    user_email: Optional[str] = None  # None for system actions
    user_role: Optional[str] = None
    action: str  # What was done
    resource_type: str  # What was affected (user, product, payment, etc.)
    resource_id: Optional[str] = None  # ID of affected resource
    details: Dict[str, Any] = {}  # Additional context
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    status: str = "success"  # success, failure, error
    error_message: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = {}


class AuditLogCreate(BaseModel):
    """Request model for creating audit log"""
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    details: Dict[str, Any] = {}
    status: str = "success"
    error_message: Optional[str] = None


class AuditLogger:
    """Manage audit logs with retention and search"""
    
    # Action types
    ACTIONS = {
        # Authentication
        'auth.login': 'User login',
        'auth.logout': 'User logout',
        'auth.register': 'User registration',
        'auth.password_change': 'Password change',
        'auth.password_reset': 'Password reset',
        'auth.2fa_enable': '2FA enabled',
        'auth.2fa_disable': '2FA disabled',
        
        # User management
        'user.create': 'User created',
        'user.update': 'User updated',
        'user.delete': 'User deleted',
        'user.role_change': 'User role changed',
        
        # Payment operations
        'payment.checkout_created': 'Checkout session created',
        'payment.payment_completed': 'Payment completed',
        'payment.payment_failed': 'Payment failed',
        'payment.refund': 'Payment refunded',
        
        # Subscription operations
        'subscription.created': 'Subscription created',
        'subscription.cancelled': 'Subscription cancelled',
        'subscription.renewed': 'Subscription renewed',
        
        # Product operations
        'product.create': 'Product created',
        'product.update': 'Product updated',
        'product.delete': 'Product deleted',
        
        # Affiliate operations
        'affiliate.register': 'Affiliate registered',
        'affiliate.link_created': 'Affiliate link created',
        'affiliate.commission_paid': 'Commission paid',
        'affiliate.payout_requested': 'Payout requested',
        
        # API Key operations
        'apikey.create': 'API key created',
        'apikey.revoke': 'API key revoked',
        'apikey.rotate': 'API key rotated',
        
        # Admin operations
        'admin.settings_change': 'Settings changed',
        'admin.user_impersonate': 'User impersonation',
        'admin.backup_created': 'Database backup created',
        'admin.data_export': 'Data exported',
        
        # Security events
        'security.rate_limit_exceeded': 'Rate limit exceeded',
        'security.invalid_token': 'Invalid token used',
        'security.suspicious_activity': 'Suspicious activity detected',
    }
    
    # Resource types
    RESOURCE_TYPES = [
        'user', 'product', 'payment', 'subscription', 'affiliate',
        'api_key', 'campaign', 'notification', 'settings', 'system'
    ]
    
    def __init__(self, db: AsyncIOMotorDatabase, retention_days: int = 90):
        self.db = db
        self.collection = db['audit_logs']
        self.retention_days = retention_days
    
    async def log(
        self,
        action: str,
        resource_type: str,
        user_email: Optional[str] = None,
        user_role: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Dict[str, Any] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        status: str = "success",
        error_message: Optional[str] = None,
        metadata: Dict[str, Any] = None
    ) -> str:
        """
        Create an audit log entry
        Returns log ID
        """
        import uuid
        
        log_entry = AuditLog(
            id=str(uuid.uuid4()),
            user_email=user_email,
            user_role=user_role,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent,
            status=status,
            error_message=error_message,
            metadata=metadata or {}
        )
        
        await self.collection.insert_one(log_entry.model_dump())
        
        # Log to file as well
        logger.info(
            f"AUDIT: {action} | User: {user_email or 'system'} | "
            f"Resource: {resource_type}/{resource_id} | Status: {status}"
        )
        
        return log_entry.id
    
    async def log_from_request(
        self,
        request,
        action: str,
        resource_type: str,
        resource_id: Optional[str] = None,
        details: Dict[str, Any] = None,
        status: str = "success",
        error_message: Optional[str] = None
    ) -> str:
        """
        Create audit log from FastAPI request
        Automatically extracts user info, IP, user agent
        """
        # Extract user info from request
        user_email = None
        user_role = None
        
        # Try to get user from request state (if authenticated)
        if hasattr(request.state, 'user'):
            user = request.state.user
            user_email = getattr(user, 'email', None)
            user_role = getattr(user, 'role', None)
        
        # Get IP and user agent
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get('user-agent')
        
        return await self.log(
            action=action,
            resource_type=resource_type,
            user_email=user_email,
            user_role=user_role,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            status=status,
            error_message=error_message
        )
    
    async def search_logs(
        self,
        user_email: Optional[str] = None,
        action: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[AuditLog]:
        """Search audit logs with filters"""
        query = {}
        
        if user_email:
            query['user_email'] = user_email
        
        if action:
            query['action'] = action
        
        if resource_type:
            query['resource_type'] = resource_type
        
        if resource_id:
            query['resource_id'] = resource_id
        
        if status:
            query['status'] = status
        
        # Date range filter
        if start_date or end_date:
            query['timestamp'] = {}
            if start_date:
                query['timestamp']['$gte'] = start_date
            if end_date:
                query['timestamp']['$lte'] = end_date
        
        cursor = self.collection.find(query).sort('timestamp', -1).skip(offset).limit(limit)
        
        logs = await cursor.to_list(length=limit)
        return [AuditLog(**log) for log in logs]
    
    async def get_user_activity(
        self,
        user_email: str,
        days: int = 30,
        limit: int = 100
    ) -> List[AuditLog]:
        """Get recent activity for a user"""
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        return await self.search_logs(
            user_email=user_email,
            start_date=start_date,
            limit=limit
        )
    
    async def get_resource_history(
        self,
        resource_type: str,
        resource_id: str,
        limit: int = 50
    ) -> List[AuditLog]:
        """Get change history for a specific resource"""
        return await self.search_logs(
            resource_type=resource_type,
            resource_id=resource_id,
            limit=limit
        )
    
    async def get_security_events(
        self,
        days: int = 7,
        limit: int = 100
    ) -> List[AuditLog]:
        """Get recent security-related events"""
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        security_actions = [
            action for action in self.ACTIONS.keys()
            if action.startswith('security.') or action.startswith('auth.')
        ]
        
        query = {
            'action': {'$in': security_actions},
            'timestamp': {'$gte': start_date}
        }
        
        cursor = self.collection.find(query).sort('timestamp', -1).limit(limit)
        logs = await cursor.to_list(length=limit)
        return [AuditLog(**log) for log in logs]
    
    async def get_failed_operations(
        self,
        days: int = 7,
        limit: int = 100
    ) -> List[AuditLog]:
        """Get recent failed operations"""
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        return await self.search_logs(
            status='failure',
            start_date=start_date,
            limit=limit
        )
    
    async def get_stats(
        self,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get audit log statistics"""
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        # Count total logs
        total = await self.collection.count_documents({
            'timestamp': {'$gte': start_date}
        })
        
        # Count by action
        action_pipeline = [
            {'$match': {'timestamp': {'$gte': start_date}}},
            {'$group': {'_id': '$action', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 10}
        ]
        action_counts = await self.collection.aggregate(action_pipeline).to_list(length=10)
        
        # Count by status
        status_pipeline = [
            {'$match': {'timestamp': {'$gte': start_date}}},
            {'$group': {'_id': '$status', 'count': {'$sum': 1}}}
        ]
        status_counts = await self.collection.aggregate(status_pipeline).to_list(length=10)
        
        # Count unique users
        unique_users = await self.collection.distinct('user_email', {
            'timestamp': {'$gte': start_date},
            'user_email': {'$ne': None}
        })
        
        return {
            'total_logs': total,
            'unique_users': len(unique_users),
            'top_actions': [
                {'action': item['_id'], 'count': item['count']}
                for item in action_counts
            ],
            'by_status': {
                item['_id']: item['count']
                for item in status_counts
            },
            'period_days': days
        }
    
    async def cleanup_old_logs(self) -> int:
        """Remove logs older than retention period"""
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=self.retention_days)
        
        result = await self.collection.delete_many({
            'timestamp': {'$lt': cutoff_date}
        })
        
        if result.deleted_count > 0:
            logger.info(f"Deleted {result.deleted_count} old audit logs")
        
        return result.deleted_count
    
    async def export_logs(
        self,
        start_date: datetime,
        end_date: datetime,
        format: str = 'json'
    ) -> str:
        """Export logs to JSON or CSV"""
        logs = await self.search_logs(
            start_date=start_date,
            end_date=end_date,
            limit=10000
        )
        
        if format == 'json':
            return json.dumps(
                [log.model_dump() for log in logs],
                default=str,
                indent=2
            )
        elif format == 'csv':
            # Simple CSV export
            import csv
            from io import StringIO
            
            output = StringIO()
            if logs:
                writer = csv.DictWriter(
                    output,
                    fieldnames=logs[0].model_dump().keys()
                )
                writer.writeheader()
                for log in logs:
                    writer.writerow(log.model_dump())
            
            return output.getvalue()
        
        raise ValueError(f"Unsupported format: {format}")
