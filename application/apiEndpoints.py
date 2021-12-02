from flask import *
from flask import current_app as app
from flask_restful import *
from .models import *
import requests

api = Api(app)


class DeckResource(Resource):
    def get(self, deck_id):         #get deck by deck id
        try:
            currentDeck = Decks.query.get(deck_id)
            if not currentDeck:
                return{'status':'error', 'message': 'deck not present'}
            cardsInDeck = Cards.query.filter_by(deck_id = deck_id)
            di = deck_id
            ui = currentDeck.user_id
            dn = currentDeck.deck_name
            ts = currentDeck.total_score
            lr = currentDeck.last_reviewed
            cards = []
            for card in cardsInDeck:
                ci = card.card_id
                f = card.front
                b = card.back
                cs = card.card_score
                tempDict = {'card_id':ci,'front':f,'back':b,'card_score':cs}
                cards.append(tempDict)
            return {'deck_id':di,'user_id':ui,'deck_name':dn,'total_score':ts,'last_reviewed':str(lr), 'cards':cards}
        except:
            abort(500)

    def put(self, deck_id):             #update deck by deck id
        try:
            try:
                json_values = request.json
            except:
                return{'status':'error', 'message': 'no update parameters'}
            di = deck_id
            currentDeck = Decks.query.get(di)
            if not currentDeck:
                return{'status':'error', 'message': 'deck not present'}
            currentDeck.deck_name = str(json_values.get('deck_name', currentDeck.deck_name))
            currentDeck.last_reviewed = (json_values.get('last_reviewed', currentDeck.last_reviewed))
            nts = json_values.get('total_score', currentDeck.total_score)
            try:
                nts = int(nts)
            except:
                return{'status':'error', 'message': 'score has to be a number'}
            currentDeck.total_score = nts
            db.session.commit()
            return{'status':'success', 'message': 'successfully updated'}
        except:
            abort(500)

    def delete(self, deck_id):          #delete deck by deck id
        try:    
            di = deck_id
            currentDeck = Decks.query.get(di)
            if not currentDeck:
                return{'status':'error', 'message': 'deck not present'}
            cardsInDeck = Cards.query.filter_by(deck_id = deck_id)
            for card in cardsInDeck:
                db.session.delete(card)
            db.session.delete(currentDeck)
            db.session.commit()
            return{'status':'success', 'message': 'successfully deleted'}
        except:
            abort(500)

class UserdeckResource(Resource):
    def get(self, user_id):         #get all decks by user id
        try:
            decks = Decks.query.filter_by(user_id = user_id)
            userdecks=[]
            for deck in decks:
                di = deck.deck_id
                tempres = requests.get('http://localhost:8080/api/decks/'+str(di))
                # tempres = {}
                userdecks.append(tempres.json())
            return jsonify(userdecks)
            # return userdecks
        except:
            abort(500)

class DeckallResource(Resource):
    def get(self):          #get all decks
        try:
            decks= Decks.query.all()
            allDecks=[]
            for deck in decks:
                di = deck.deck_id
                deckValue = requests.get('http://localhost:8080/api/decks/'+str(di))
                allDecks.append(deckValue.json())
            return allDecks

        except:
            abort(500)

    def post(self):         #create new deck
        try:
            try:
                json_values = request.json
            except:
                return{'status':'error', 'message': 'no update parameters'}
            dn = json_values.get('deck_name', False)
            ui = json_values.get('user_id', False)
            if not dn:
                return{'status':'error', 'message': 'deck name required'}
            if not ui:
                return{'status':'error', 'message': 'user id required'}
            try:
                ui = int(ui)
            except:
                return{'status':'error', 'message': 'user id should be a number'}
            userPresent = Users.query.get(ui)
            if not userPresent:
                return{'status':'error', 'message': 'User not present. Add user first'}
            currentDeck = Decks.query.filter_by(deck_name=dn).first()
            try:
                if currentDeck.user_id == ui:
                    return{'status':'error', 'message': 'deck already present. Try updating it'}
                else:
                    return{'status':'error', 'message': 'deck name already exists. Choose a different name'}
            except:
                pass
            newDeck = Decks(dn, ui)
            db.session.add(newDeck)
            db.session.commit()
            return {'status':'success', 'message': 'successfully created'}
        except:
            abort(500)

class CardResource(Resource):
    def get(self, card_id):     #get card by card id
        try:
            currentCard = Cards.query.get(card_id)
            if not currentCard:
                return{'status':'error', 'message': 'Card not present'}
            ci = currentCard.card_id
            di = currentCard.deck_id
            f = currentCard.front
            b = currentCard.back
            cs = currentCard.card_score
            return {'deck_id':di,'card_id':ci,'front':f,'back':b,'card_score':cs}
        except:
            abort(500)

    def put(self, card_id):         #update card by card id
        try:
            try:
                json_values = request.json
            except:
                return{'status':'error', 'message': 'no update parameters'}
            ci = card_id
            currentCard = Cards.query.get(ci)
            if not currentCard:
                return{'status':'error', 'message': 'card not present'}
            currentCard.front = str(json_values.get('front', currentCard.front))
            currentCard.back = str(json_values.get('back', currentCard.back))
            ns = json_values.get('card_score', currentCard.card_score)
            try:
                ns = int(ns)
            except:
                return{'status':'error', 'message': 'score has to be a number'}
            currentCard.card_score = ns
            db.session.commit()
            return{'status':'success', 'message': 'successfully updated'}
        except:
            abort(500)

    def delete(self, card_id):              #delete card by card id
        try:
            ci = card_id
            currentCard = Cards.query.get(ci)
            if not currentCard:
                return{'status':'error', 'message': 'card not present'}
            db.session.delete(currentCard)
            db.session.commit()
            return{'status':'success', 'message': 'successfully deleted'}
        except:
            abort(500)

class CardallResource(Resource):
    def post(self):                 #create new card 
        try:
            try:
                json_values = request.json
            except:
                return{'status':'error', 'message': 'no update parameters'}
            di = json_values.get('deck_id', False)
            f = json_values.get('front', False)
            b = json_values.get('back', False)
            if not di:
                return{'status':'error', 'message': 'deck id required'}
            if not f:
                return{'status':'error', 'message': 'front value required'}
            if not b:
                return{'status':'error', 'message': 'back value required'}
            try:
                di = int(di)
            except:
                return{'status':'error', 'message': 'deck id should be a number'}
            deckPresent = Decks.query.get(di)
            if not deckPresent:
                return{'status':'error', 'message': 'Deck not present. Add deck first'}

            currentDeck = Cards.query.filter_by(deck_id=di)
            for currentCard in currentDeck:
                if currentCard.front == f:
                    return{'status':'error', 'message': 'card already present. Try updating it'}
            newCard = Cards(di, f, b)
            db.session.add(newCard)
            db.session.commit()
            return {'status':'success', 'message': 'successfully created'}
        except:
            abort(500)

class DeckcardResource(Resource):
    def get(self, deck_id):                  #get card by deck id
        try:
            deckPresent = Decks.query.get(deck_id)
            if not deckPresent:
                return{'status':'error', 'message': 'Deck not present'}
            cards=[]
            currentDeck = Cards.query.filter_by(deck_id=deck_id)
            for currentCard in currentDeck:
                ci = currentCard.card_id
                tempres = requests.get('http://localhost:8080/api/cards/'+str(ci))
                cards.append(tempres.json())
            return cards
        except:
            abort(500)
        
class UserResource(Resource):
    def get(self, user_id):             #get user details
        try:
            currentUser = Users.query.get(user_id)
            if not currentUser:
                return{'status':'error', 'message': 'User not present'}
            return{'username':currentUser.username, 'passeword':currentUser.password}
        except:
            abort(500)

    def put(self, user_id):         #update user details
        try:
            try:
                json_values = request.json
            except:
                return{'status':'error', 'message': 'no update parameters'}
            currentUser = Users.query.get(user_id)
            if not currentUser:
                return{'status':'error', 'message': 'User not present'}
            currentUser.username = json_values.get('username', currentUser.username)
            currentUser.password = json_values.get('password', currentUser.password)
            db.session.commit()
            return{'status':'success', 'message': 'successfully updated'}
        except:
            abort(500)

    def delete(self, user_id):           #delete user
        try:    
            currentUser = Users.query.get(user_id)
            if not currentUser:
                return{'status':'error', 'message': 'User not present'}
            userdecks = Decks.query.filter_by(user_id = user_id)
            for deck in userdecks:
                di = deck.deck_id
                tempres = requests.delete('http://localhost:8080/api/decks/'+str(di))
            db.session.delete(currentUser)
            db.session.commit()
            return{'status':'success', 'message': 'successfully deleted'}
        except:
            abort(500)

class UserallResource(Resource):
    def post(self):             #add user
        try:
            try:
                json_values = request.json
            except:
                return{'status':'error', 'message': 'no update parameters'}
            un = json_values.get('username', False)
            pwd = json_values.get('password', False)
            if not un:
                return{'status':'error', 'message': 'username required'}
            if not pwd:
                return{'status':'error', 'message': 'password required'}
            currentUser = Users.query.filter_by(username=un).first()
            if currentUser:
                return{'status':'error', 'message': 'User already present'}
            newUser = Users(un,pwd)
            db.session.add(newUser)
            db.session.commit()
            return{'status':'success', 'message': 'successfully created'}
        except:
            abort(500)




api.add_resource(DeckResource, '/api/decks/<int:deck_id>')
api.add_resource(DeckallResource, '/api/decks')
api.add_resource(UserdeckResource, '/api/user/decks/<int:user_id>')
api.add_resource(CardResource, '/api/cards/<int:card_id>')
api.add_resource(CardallResource, '/api/cards')
api.add_resource(DeckcardResource, '/api/decks/cards/<int:deck_id>')
api.add_resource(UserResource, '/api/user/<int:user_id>')
api.add_resource(UserallResource, '/api/user')
