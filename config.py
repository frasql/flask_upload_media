import os
from dotenv import load_dotenv
import datetime

load_dotenv()


BASEDIR = os.path.dirname(os.path.abspath(__file__))


class BaseConfig:
    DEBUG = True
    TESTING = False

    SECRET_KEY = os.getenv("SECRET_KEY")
    PROPAGATE_EXCEPTIONS = True  # bubble propagation

    SESSION_COOKIE_SECURE = False

    PDF_FOLDER = os.path.join(BASEDIR, 'static/client/pdf')
    
    DATABASE_LOG_FILE = os.path.join(BASEDIR, 'static/log/application.log')

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]


class TestingConfig(BaseConfig):
    TESTING = True
    DUBUG = False
    
    DB_TEST_USER = os.getenv('DB_TEST_USER')
    DB_TEST_PASSWORD = os.getenv('DB_TEST_PASSWORD')
    DB_TEST_HOST = os.getenv('DB_TEST_HOST')
    DB_TEST_DATABASE = os.getenv('DB_TEST_DATABASE')
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{DB_TEST_USER}:{DB_TEST_PASSWORD}@{DB_TEST_HOST}/{DB_TEST_DATABASE}"
    )


class ProductionConfig(BaseConfig):
    # app configuration
    DEBUG = False
    TESTING = False

    # db configuration
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_DATABASE = os.getenv('DB_DATABASE')
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # jwt configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')


    SESSION_COOKIE_SECURE = True

    # satic folder configuration
    PDF_FOLDER = os.path.join(BASEDIR, 'static/client/pdf')
    LOG_FILE = os.path.join(BASEDIR, 'static/log')


class SimpleTestConfig(BaseConfig):
    # sqlalchemy configuration
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = "invwonruivbriuvbieurvbeirvbebrie"
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=1800)
    JWT_COOKIE_SECURE = False 
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=15)
    JWT_COOKIE_CSRF_PROTECT = True 
    JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN-ACCESS"
    JWT_REFRESH_CSRF_HEADER_NAME = "X-CSRF-TOKEN-REFRESH"
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_CSRF_CHECK_FORM = True    

    # jwt blacklist configuration
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]