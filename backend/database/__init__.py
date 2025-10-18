"""
Database optimization package
Provides migrations, backups, and performance utilities
"""
from .migrations import run_all_migrations, MigrationManager
from .backup import MongoBackupManager

__all__ = ['run_all_migrations', 'MigrationManager', 'MongoBackupManager']
