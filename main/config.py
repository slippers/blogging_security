import os

class BaseConfig(object):
    # directory above configure 
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    # configuration
    DEBUG = False
    TESTING = False

    SQLALCHEMY_ECHO = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir,'database', 'wordnet-31.db')

    SQLALCHEMY_ENGINE = 'sqlite://'

    SQLALCHEMY_BINDS = {
            'blog': 'sqlite:///' + os.path.join(basedir,'database', 'blog.db'),
            'security': 'sqlite:///' + os.path.join(basedir,'database', 'security.db')
            }

    SECRET_KEY = "secret"  # for WTF-forms and login
    BLOGGING_URL_PREFIX = "/blog"
    BLOGGING_DISQUS_SITENAME = "test"
    BLOGGING_SITEURL = "http://localhost:8000"

class DevelopmentConfig(BaseConfig):
    DEBUG = True    
    TESTING = True
    SQLALCHEMY_ECHO = False

class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True


config = {
        "development": "main.config.DevelopmentConfig",
        "testing": "main.config.TestingConfig",
        "default": "main.config.DevelopmentConfig"
        }

def configure_app(app):
    config_name = os.getenv('FLAKS_CONFIGURATION', 'default')
    print(config[config_name])
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)
