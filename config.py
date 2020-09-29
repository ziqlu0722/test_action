import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] or "postgresql://localhost/webapp_db"
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/webapp_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'webapp_test_db')
    if os.environ.get('GITHUB_WORKFLOW'):
        SQLALCHEMY_DATABASE_URI = DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=postgres,
                                                                                        pw=postgres,
                                                                                        url=localhost:5432,
                                                                                        db=github_actions)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
