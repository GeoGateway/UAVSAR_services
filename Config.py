import os

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    WTF_CSRF_ENABLED = True
    
    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    DEVMODE=False
    METADATA=os.path.join(BASE_DIR, 'Data/metadata.geojson'),
    pass

class DevelopmentConfig(Config):
    """Statement for enabling the development environment"""
    #setup metadata
    #METADATA = os.path.join(BASE_DIR,"Data","metadata.geojson")
    METADATA=os.path.join(BASE_DIR, 'Data/metadata.geojson'),
    DEVMODE=True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
