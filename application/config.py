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

class ProductionConfig(Config):     # replace any of below only if using separate DB server in a production env
    user = 'YourUser'               # replace with your postgres of other DB user
    password = 'YourPassword'       #replace with its password
    host = 'localhost'              #replace with DB server IP                              
    port = 5432                     #replace DB Server Port
    database = 'YourDB'             #replace with database name
    SQLALCHEMY_DATABASE_URI = ('postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, database))
    DEBUG = False
