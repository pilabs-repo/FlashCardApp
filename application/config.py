import os

baseDir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevConfig(Config):
    SQLITE_DB_DIR = os.path.join(baseDir, "../data")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, 'testdb.sqlite3')
    DEBUG = True

class ProductionConfig(Config):
    user = 'flashcardApp'
    password = 'flashtest@123'
    host = 'localhost'
    port = 5432
    database = 'flashCardDB'
    SQLALCHEMY_DATABASE_URI = ('postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, database))
    DEBUG = False