#define database 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative.api import declarative_base

Base = declarative_base()
db = SQLAlchemy()