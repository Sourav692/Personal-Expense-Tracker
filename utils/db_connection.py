"""
Database Connection Utility Module
Provides secure database connection management with pooling and error handling.
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from contextlib import contextmanager
from dotenv import load_dotenv
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Load environment variables
load_dotenv()


class DatabaseConnection:
    """
    Secure database connection manager with error handling and resource cleanup.
    Supports connection pooling for production use.
    """
    
    def __init__(self, connection_string: str, pool_size: int = 5, max_overflow: int = 10):
        """
        Initialize database connection manager.
        
        Args:
            connection_string: PostgreSQL connection string
            pool_size: Number of connections to maintain in pool
            max_overflow: Maximum overflow connections
        """
        self.connection_string = connection_string
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self._pool: Optional[ThreadedConnectionPool] = None
        self._engine = None
    
    def create_pool(self) -> ThreadedConnectionPool:
        """Create a connection pool."""
        if self._pool is None:
            try:
                from urllib.parse import urlparse
                parsed = urlparse(self.connection_string)
                
                # Extract SSL mode from query string
                ssl_mode = 'require'
                if parsed.query:
                    for param in parsed.query.split('&'):
                        if param.startswith('sslmode='):
                            ssl_mode = param.split('=')[1]
                            break
                
                self._pool = ThreadedConnectionPool(
                    minconn=1,
                    maxconn=self.pool_size,
                    host=parsed.hostname,
                    port=parsed.port or 5432,
                    database=parsed.path[1:] if parsed.path else 'postgres',
                    user=parsed.username,
                    password=parsed.password,
                    sslmode=ssl_mode
                )
            except Exception as e:
                raise ConnectionError(f"Failed to create connection pool: {str(e)}")
        return self._pool
    
    def get_connection(self):
        """Get a connection from the pool."""
        if self._pool is None:
            self.create_pool()
        
        try:
            return self._pool.getconn()
        except Exception as e:
            raise ConnectionError(f"Failed to get connection from pool: {str(e)}")
    
    def return_connection(self, conn):
        """Return a connection to the pool."""
        if self._pool:
            try:
                self._pool.putconn(conn)
            except Exception as e:
                print(f"Warning: Error returning connection to pool: {str(e)}")
    
    @contextmanager
    def get_cursor(self, commit: bool = False):
        """
        Context manager for database cursor with automatic cleanup.
        
        Args:
            commit: Whether to commit transaction on exit
        
        Yields:
            Database cursor
        """
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            yield cursor
            if commit:
                conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise ConnectionError(f"Database operation failed: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                self.return_connection(conn)
    
    def get_sqlalchemy_engine(self):
        """Get SQLAlchemy engine with connection pooling."""
        if self._engine is None:
            try:
                self._engine = create_engine(
                    self.connection_string,
                    poolclass=QueuePool,
                    pool_size=self.pool_size,
                    max_overflow=self.max_overflow,
                    pool_pre_ping=True,
                    echo=False
                )
            except Exception as e:
                raise ConnectionError(f"Failed to create SQLAlchemy engine: {str(e)}")
        return self._engine
    
    def close_all(self):
        """Close all connections and cleanup resources."""
        if self._pool:
            try:
                self._pool.closeall()
            except Exception as e:
                print(f"Warning: Error closing pool: {str(e)}")
        
        if self._engine:
            try:
                self._engine.dispose()
            except Exception as e:
                print(f"Warning: Error disposing engine: {str(e)}")


def load_lakebase_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load Lakebase configuration from JSON file.
    
    Args:
        config_path: Path to configuration file
    
    Returns:
        Configuration dictionary
    """
    if config_path is None:
        config_path = Path(__file__).parent.parent / "configuration" / "lakebase-config.json"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        return json.load(f)


def get_credentials(config: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    """
    Get database credentials with fallback priority:
    1. Environment variables (most secure)
    2. Configuration file (development only)
    
    Args:
        config: Optional configuration dictionary
    
    Returns:
        Dictionary with username and password
    """
    if config is None:
        config = load_lakebase_config()
    
    # Priority 1: Environment variables
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    
    if username and password:
        return {"username": username, "password": password}
    
    # Priority 2: Configuration file
    conn_config = config.get('connection', {})
    credentials = conn_config.get('credentials', {})
    
    if credentials.get('username') and credentials.get('password'):
        return credentials
    
    raise ValueError(
        "No database credentials found. Set DB_USERNAME and DB_PASSWORD "
        "environment variables."
    )


def build_connection_string(
    host: str,
    port: int,
    database: str,
    username: str,
    password: str,
    ssl_mode: str = "require"
) -> str:
    """
    Build a secure PostgreSQL connection string with SSL support.
    
    Args:
        host: Database host
        port: Database port
        database: Database name
        username: Database username
        password: Database password
        ssl_mode: SSL mode (require, verify-ca, verify-full)
    
    Returns:
        PostgreSQL connection string
    """
    return f"postgresql://{username}:{password}@{host}:{port}/{database}?sslmode={ssl_mode}"


def get_connection_string(config: Optional[Dict[str, Any]] = None) -> str:
    """
    Get connection string from configuration.
    
    Args:
        config: Optional configuration dictionary
    
    Returns:
        PostgreSQL connection string
    """
    if config is None:
        config = load_lakebase_config()
    
    conn_config = config.get('connection', {})
    credentials = get_credentials(config)
    
    host = conn_config.get('host')
    port = conn_config.get('port', 5432)
    database = conn_config.get('database', 'postgres')
    ssl_mode = conn_config.get('ssl_mode', 'require')
    
    if not host:
        raise ValueError("Database host not found in configuration")
    
    return build_connection_string(
        host=host,
        port=port,
        database=database,
        username=credentials['username'],
        password=credentials['password'],
        ssl_mode=ssl_mode
    )


def test_connection(connection_string: str) -> Dict[str, Any]:
    """
    Test database connection.
    
    Args:
        connection_string: PostgreSQL connection string
    
    Returns:
        Dictionary with test results
    """
    import time
    import psycopg2
    
    results = {
        "success": False,
        "postgresql_version": None,
        "database_name": None,
        "current_user": None,
        "ssl_enabled": None,
        "connection_time_ms": None,
        "error": None
    }
    
    start_time = time.time()
    
    try:
        conn = psycopg2.connect(connection_string)
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT version();")
            results["postgresql_version"] = cursor.fetchone()[0]
            
            cursor.execute("SELECT current_database();")
            results["database_name"] = cursor.fetchone()[0]
            
            cursor.execute("SELECT current_user;")
            results["current_user"] = cursor.fetchone()[0]
            
            cursor.execute("SHOW ssl;")
            ssl_status = cursor.fetchone()[0]
            results["ssl_enabled"] = ssl_status == "on"
        
        conn.close()
        results["success"] = True
        results["connection_time_ms"] = round((time.time() - start_time) * 1000, 2)
        
    except Exception as e:
        results["error"] = str(e)
        results["success"] = False
    
    return results

