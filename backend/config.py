import os
import dotenv

dotenv.load_dotenv()

class Config:
    """Base config."""
    
class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    # Development-specific settings
    TIKTOK_CLIENT_KEY=os.environ.get('TIKTOK_CLIENT_KEY')
    TIKTOK_CLIENT_SECRET=os.environ.get('TIKTOK_CLIENT_SECRET')
    TIKTOK_REDIRECT_URI=os.environ.get('TIKTOK_REDIRECT_URI')

    OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')

    INSTAGRAM_TOKEN=os.environ.get('INSTAGRAM_TOKEN')


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    # Production-specific settings
    TIKTOK_CLIENT_KEY=os.environ.get('TIKTOK_CLIENT_KEY')
    TIKTOK_CLIENT_SECRET=os.environ.get('TIKTOK_CLIENT_SECRET')
    TIKTOK_REDIRECT_URI=os.environ.get('TIKTOK_REDIRECT_URI')

    OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')
    
    INSTAGRAM_TOKEN=os.environ.get('INSTAGRAM_TOKEN')

# Dictionary to map config names to config classes
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
