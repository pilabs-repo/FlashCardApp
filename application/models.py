# database models/table definitions
from .database import *


class Users(db.Model):
    __tablename__='users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    def __init__(self, un, pwd):
        self.username = un
        self.password = pwd

class Decks(db.Model):
    __tablename__='decks'
    deck_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deck_name = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    total_score = db.Column(db.Integer, nullable =True)
    last_reviewed = db.Column(db.DateTime(timezone=True), nullable = True)
    def __init__(self, dn, ui):
        self.deck_name = dn
        self.user_id = ui
        self.total_score = 0
        self.last_reviewed = None

class Cards(db.Model):
    __tablename__='cards'
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deck_id = db.Column(db.Integer, db.ForeignKey("decks.deck_id"), nullable=False)
    front = db.Column(db.String(50), unique = True, nullable=False)
    back = db.Column(db.String(50), nullable=False)
    card_score = db.Column(db.Integer, nullable=False)
    def __init__(self, di, f, b):
        self.deck_id = di
        self.front = f
        self.back = b
        self.card_score = 0

        
db.create_all()
db.session.commit()
