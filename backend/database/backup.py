"""
MongoDB Backup System
Automated backup with compression and retention policies
"""
import os
import subprocess
import logging
from datetime import datetime, timedelta
from pathlib import Path
import shutil
import glob
from typing import Optional

logger = logging.getLogger(__name__)


class MongoBackupManager:
    """Manages MongoDB backups with compression and retention"""
    
    def __init__(
        self, 
        mongo_url: str, 
        db_name: str,
        backup_dir: str = "/app/backups",
        retention_days: int = 7,
        max_backups: int = 10
    ):
        self.mongo_url = mongo_url
        self.db_name = db_name
        self.backup_dir = Path(backup_dir)
        self.retention_days = retention_days
        self.max_backups = max_backups
        
        # Create backup directory if not exists
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def create_backup(self) -> Optional[str]:
        """
        Create a compressed backup of the database
        Returns path to backup file or None on error
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{self.db_name}_backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        compressed_path = f"{backup_path}.tar.gz"
        
        try:
            logger.info(f"🔄 Starting backup: {backup_name}")
            
            # Run mongodump
            cmd = [
                "mongodump",
                "--uri", self.mongo_url,
                "--db", self.db_name,
                "--out", str(backup_path),
                "--gzip"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode != 0:
                logger.error(f"❌ Mongodump failed: {result.stderr}")
                return None
            
            # Compress backup directory
            logger.info(f"📦 Compressing backup...")
            shutil.make_archive(
                str(backup_path),
                'gztar',
                str(backup_path)
            )
            
            # Remove uncompressed directory
            shutil.rmtree(backup_path)
            
            # Get backup size
            size_mb = Path(compressed_path).stat().st_size / (1024 * 1024)
            
            logger.info(f"✅ Backup created: {compressed_path} ({size_mb:.2f} MB)")
            return compressed_path
            
        except subprocess.TimeoutExpired:
            logger.error(f"❌ Backup timeout after 5 minutes")
            return None
        except Exception as e:
            logger.error(f"❌ Backup failed: {e}")
            return None
    
    def cleanup_old_backups(self):
        """Remove old backups based on retention policy"""
        try:
            # Get all backup files
            backup_files = sorted(
                glob.glob(str(self.backup_dir / f"{self.db_name}_backup_*.tar.gz")),
                key=os.path.getmtime,
                reverse=True
            )
            
            cutoff_date = datetime.now() - timedelta(days=self.retention_days)
            removed_count = 0
            
            # Remove backups older than retention period or exceeding max count
            for i, backup_file in enumerate(backup_files):
                backup_path = Path(backup_file)
                file_time = datetime.fromtimestamp(backup_path.stat().st_mtime)
                
                should_remove = (
                    file_time < cutoff_date or
                    i >= self.max_backups
                )
                
                if should_remove:
                    backup_path.unlink()
                    removed_count += 1
                    logger.info(f"🗑️  Removed old backup: {backup_path.name}")
            
            if removed_count > 0:
                logger.info(f"✅ Cleaned up {removed_count} old backups")
            
        except Exception as e:
            logger.error(f"❌ Cleanup failed: {e}")
    
    def list_backups(self):
        """List all available backups"""
        backup_files = sorted(
            glob.glob(str(self.backup_dir / f"{self.db_name}_backup_*.tar.gz")),
            key=os.path.getmtime,
            reverse=True
        )
        
        if not backup_files:
            logger.info("📦 No backups found")
            return []
        
        logger.info("=" * 60)
        logger.info(f"📦 Available backups ({len(backup_files)}):")
        logger.info("=" * 60)
        
        backups = []
        for backup_file in backup_files:
            backup_path = Path(backup_file)
            size_mb = backup_path.stat().st_size / (1024 * 1024)
            modified = datetime.fromtimestamp(backup_path.stat().st_mtime)
            
            backup_info = {
                'path': str(backup_path),
                'name': backup_path.name,
                'size_mb': size_mb,
                'modified': modified
            }
            backups.append(backup_info)
            
            logger.info(
                f"  {backup_path.name} "
                f"({size_mb:.2f} MB) - "
                f"{modified.strftime('%Y-%m-%d %H:%M:%S')}"
            )
        
        logger.info("=" * 60)
        return backups
    
    def restore_backup(self, backup_path: str):
        """
        Restore database from backup
        WARNING: This will replace the current database!
        """
        try:
            backup_path = Path(backup_path)
            if not backup_path.exists():
                logger.error(f"❌ Backup file not found: {backup_path}")
                return False
            
            logger.warning(f"⚠️  Restoring backup: {backup_path.name}")
            logger.warning(f"⚠️  This will REPLACE the current database!")
            
            # Extract backup
            extract_dir = self.backup_dir / "restore_temp"
            extract_dir.mkdir(exist_ok=True)
            
            shutil.unpack_archive(backup_path, extract_dir)
            
            # Find the database directory
            db_backup_path = extract_dir / self.db_name
            
            # Run mongorestore
            cmd = [
                "mongorestore",
                "--uri", self.mongo_url,
                "--db", self.db_name,
                "--drop",  # Drop existing collections
                "--gzip",
                str(db_backup_path)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            # Cleanup temp directory
            shutil.rmtree(extract_dir)
            
            if result.returncode != 0:
                logger.error(f"❌ Mongorestore failed: {result.stderr}")
                return False
            
            logger.info(f"✅ Database restored from: {backup_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Restore failed: {e}")
            return False
    
    def run_backup_job(self):
        """Full backup job: backup + cleanup"""
        logger.info("=" * 60)
        logger.info("🚀 Starting automated backup job")
        logger.info("=" * 60)
        
        # Create backup
        backup_path = self.create_backup()
        
        if backup_path:
            # Cleanup old backups
            self.cleanup_old_backups()
            
            # List current backups
            self.list_backups()
            
            logger.info("=" * 60)
            logger.info("✅ Backup job completed successfully")
            logger.info("=" * 60)
            return True
        else:
            logger.error("❌ Backup job failed")
            return False


# =========================
# CLI INTERFACE
# =========================

if __name__ == "__main__":
    import sys
    import argparse
    from dotenv import load_dotenv
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    load_dotenv()
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME')
    
    if not mongo_url or not db_name:
        logger.error("❌ MONGO_URL and DB_NAME must be set in environment")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description='MongoDB Backup Manager')
    parser.add_argument(
        'action',
        choices=['backup', 'list', 'restore', 'cleanup'],
        help='Action to perform'
    )
    parser.add_argument(
        '--backup-file',
        help='Backup file path (for restore action)'
    )
    parser.add_argument(
        '--retention-days',
        type=int,
        default=7,
        help='Backup retention period in days (default: 7)'
    )
    parser.add_argument(
        '--max-backups',
        type=int,
        default=10,
        help='Maximum number of backups to keep (default: 10)'
    )
    
    args = parser.parse_args()
    
    manager = MongoBackupManager(
        mongo_url=mongo_url,
        db_name=db_name,
        retention_days=args.retention_days,
        max_backups=args.max_backups
    )
    
    if args.action == 'backup':
        manager.run_backup_job()
    
    elif args.action == 'list':
        manager.list_backups()
    
    elif args.action == 'cleanup':
        manager.cleanup_old_backups()
    
    elif args.action == 'restore':
        if not args.backup_file:
            logger.error("❌ --backup-file is required for restore action")
            sys.exit(1)
        manager.restore_backup(args.backup_file)
