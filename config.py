import os 

class Config():
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] or "postgresql://localhost/webapp_db"
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/webapp_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/webapp_test_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
