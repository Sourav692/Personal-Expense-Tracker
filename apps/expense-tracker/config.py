"""
Configuration module for the Expense Tracker app.
"""

import os
import json
from pathlib import Path

class Config:
    """Application configuration."""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent.parent
    CONFIG_DIR = BASE_DIR / "configuration"
    
    # Configuration files
    LAKEBASE_CONFIG_FILE = CONFIG_DIR / "lakebase-config.json"
    APP_CONFIG_FILE = CONFIG_DIR / "app-config.json"
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    @classmethod
    def load_lakebase_config(cls):
        """Load Lakebase configuration."""
        if cls.LAKEBASE_CONFIG_FILE.exists():
            with open(cls.LAKEBASE_CONFIG_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    @classmethod
    def load_app_config(cls):
        """Load application configuration."""
        if cls.APP_CONFIG_FILE.exists():
            with open(cls.APP_CONFIG_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    @classmethod
    def get_db_connection_string(cls):
        """Get database connection string from configuration."""
        config = cls.load_lakebase_config()
        return config.get('connection', {}).get('connection_string')
    
    @classmethod
    def get_lakehouse_config(cls):
        """Get Lakehouse configuration."""
        app_config = cls.load_app_config()
        return app_config.get('lakehouse', {})

