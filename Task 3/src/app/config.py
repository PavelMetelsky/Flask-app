import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey')
    
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/0')

class DevelopmentConfig(Config):
    """Configuration for development"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuration for production"""
    DEBUG = False

class TestingConfig(Config):
    """Configuration for testing"""
    TESTING = True
    REDIS_URL = 'redis://localhost:6379/0'
