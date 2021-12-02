#setup server endpoints and control structures
from flask import *
from flask import current_app as app
from .models import *
import requests
from datetime import datetime


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        given_name = request.form.get('username')
        given_pwd = request.form.get('password')
        given_reenter_pwd = request.form.get('password2')
        if given_pwd != given_reenter_pwd:
            statuses=['Passwords do not match']
            return render_template('signup.html', statuses = statuses)
        res = requests.post('http://localhost:8080/api/user', json = {'username':given_name, 'password':given_pwd})
        if res.json().get('status')=='success':
            statuses = [res.json().get('message')]
            return render_template('login.html', statuses = statuses)
        elif res.json().get('status')=='error':
            statuses = [res.json().get('message', 'unknown error')]
            return render_template('login.html', statuses = statuses)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        try:
            uid = int(request.cookies.get('userID'))
        except:
            return render_template('login.html', statuses = [])
        if uid != -1:
            return redirect('/dashboard')
        return render_template('login.html', statuses = [])
        
    else:
        given_name = request.form.get('username')
        given_pwd = request.form.get('password')
        userobj = Users.query.filter_by(username = given_name).first()
        if not userobj:
            statuses=['User does not exist']
            return  render_template('login.html', statuses = statuses)
        if given_pwd != userobj.password:
            statuses=['Incorrect Password']
            return  render_template('login.html', statuses = statuses)

        resp = make_response(redirect('/dashboard'))
        resp.set_cookie('userID', str(userobj.user_id), max_age=600)
        return resp

@app.route("/dashboard", methods=['GET'])
def dashboard():
    try:
        uid = int(request.cookies.get('userID'))
    except:
        statuses=['Login into your account']
        return  render_template('login.html', statuses = statuses)
    if uid == -1:
        statuses=['Login into your account']
        return  render_template('login.html', statuses = statuses)
    user = Users.query.get(uid)
    resp = requests.get('http://localhost:8080/api/user/decks/'+str(uid))
    toReturn = make_response(render_template('dashboard.html',values = resp.json(), username = user.username))
    toReturn.set_cookie('userID', str(uid), max_age=600)
    return  toReturn
    
@app.route("/logout", methods=['GET'])
def logout():
    resp = make_response(redirect('/'))
    resp.set_cookie('userID', str(-1))
    return resp


def authDeckAccess(deck_id):
    try:
        uid = int(request.cookies.get('userID'))
    except:
        return 1
    if uid == -1:
        return 1
    currentDeck = Decks.query.get(deck_id)
    if not currentDeck:
        return 3
    if currentDeck.user_id != uid:
        return  2
    return 4



@app.route("/decks/<int:deck_id>", methods=['GET'])
def deckDisplay(deck_id):               #view deck
    if authDeckAccess(deck_id) ==1:
        statuses=['Login into your account']
        return  render_template('login.html', statuses = statuses)
    elif authDeckAccess(deck_id) ==2:
        return  render_template('error.html', value = ['You are not authenticated'])

    resp = requests.get('http://localhost:8080/api/decks/'+str(deck_id))
    return  render_template('deckshow.html', value= resp.json())

def updateDeckScore(deck_id):
    totS=0
    cards = requests.get('http://localhost:8080/api/decks/cards/'+str(deck_id))
    cards = cards.json()
    for card in cards:
        totS+=card['card_score']
    update = requests.put('http://localhost:8080/api/decks/'+str(deck_id), json={'total_score':totS})
ccv=0 

@app.route("/decks/review/<int:deck_id>", methods=['GET', 'POST'])
def deckReview(deck_id):       #review deck card-by-card
    global ccv
    if request.method =='GET':
        ccv =0

        if authDeckAccess(deck_id) ==1:
            statuses=['Login into your account']
            return  render_template('login.html', statuses = statuses)
        elif authDeckAccess(deck_id) ==3:
            return  render_template('error.html', value = ['Deck not present'])
        elif authDeckAccess(deck_id) ==2:
            return  render_template('error.html', value = ['You are not authenticated'])

        cards = requests.get('http://localhost:8080/api/decks/cards/'+str(deck_id))
        cards = cards.json()
        try:
            if cards['status'] == 'error':
                return  render_template('error.html', value = cards['message'])
        except:
            pass
        if ccv >= len(cards):
            return redirect('/dashboard')
        return  render_template('cardreview.html', card=cards[ccv])
    else:
        cid = int(request.form.get('card_id'))
        if request.form.get('difficulty') == 'easy':
            score = 10
        elif request.form.get('difficulty') == 'medium':
            score = 5
        elif request.form.get('difficulty') == 'hard':
            score = 1
        update = requests.put('http://localhost:8080/api/cards/'+str(cid), json={'card_score':score})
        updateDeckScore(deck_id)
        lr = datetime.now()
        # lr = lr.isoformat()
        currentDeck = Decks.query.get(deck_id)
        currentDeck.last_reviewed = lr
        db.session.commit()
        # lr = lr.isoformat()
        # update = requests.put('http://localhost:8080/api/decks/'+str(deck_id), json={'last_reviewed':lr})
        ccv=ccv+1
        if authDeckAccess(deck_id) ==1:
            statuses=['Login into your account']
            return  render_template('login.html', statuses = statuses)
        elif authDeckAccess(deck_id) ==3:
            return  render_template('error.html', value = ['Deck not present'])
        elif authDeckAccess(deck_id) ==2:
            return  render_template('error.html', value = ['You are not authenticated'])

        cards = requests.get('http://localhost:8080/api/decks/cards/'+str(deck_id))
        cards = cards.json()
        try:
            if cards['status'] == 'error':
                return  render_template('error.html', value = cards['message'])
        except:
            pass
        if ccv<len(cards):
            return  render_template('cardreview.html', card = cards[ccv])
        resp = make_response(redirect('/dashboard'))
        resp.set_cookie('userID', str(int(request.cookies.get('userID'))), max_age=600)
        return resp


@app.route("/decks/add", methods=['GET', 'POST'])
def addDeck():
    if request.method =='GET':
        try:
            uid = int(request.cookies.get('userID'))
        except:
            statuses=['Login into your account']
            return  render_template('login.html', statuses = statuses)
        return  render_template('adddeck.html', uid = uid)
    else:
        values = request.form
        try:
            uid = int(request.cookies.get('userID'))
        except:
            statuses=['Login into your account']
            return  render_template('login.html', statuses = statuses)
        if uid==-1:
            statuses=['Login into your account']
            return  render_template('login.html', statuses = statuses)

        update = requests.post('http://localhost:8080/api/decks', json={'deck_name':values.get('deck_name'), 'user_id':uid})
        return redirect('/dashboard')
        



@app.route("/decks/edit/<int:deck_id>", methods=['GET', 'POST'])
def editDeck(deck_id):
    if request.method =='GET':
        deck = Decks.query.get(deck_id)
        return  render_template('editdeck.html', di=deck_id, dn = deck.deck_name)
    else:
        if authDeckAccess(deck_id) ==1:
            statuses=['Login into your account']
            return  render_template('login.html', statuses = statuses)
        elif authDeckAccess(deck_id) ==3:
            return  render_template('error.html', value = ['Deck not present'])
        elif authDeckAccess(deck_id) ==2:
            return  render_template('error.html', value = ['You are not authenticated'])
        ndn = request.form.get('deck_name')
        resp = requests.put('http://localhost:8080/api/decks/'+str(deck_id), json={'deck_name':ndn})
        return  redirect('/dashboard')
    


@app.route("/decks/delete/<int:deck_id>", methods=['GET'])
def deckDelete(deck_id):
    if authDeckAccess(deck_id) ==1:
        statuses=['Login into your account']
        return  render_template('login.html', statuses = statuses)
    elif authDeckAccess(deck_id) ==3:
        return  render_template('error.html', value = ['Deck not present'])
    elif authDeckAccess(deck_id) ==2:
        return  render_template('error.html', value = ['You are not authenticated'])


    resp = requests.delete('http://localhost:8080/api/decks/'+str(deck_id))
    return  redirect('/dashboard')


@app.route("/decks/export/<int:deck_id>", methods=['GET'])
def deckExport(deck_id):
    if authDeckAccess(deck_id) ==1:
        statuses=['Login into your account']
        return  render_template('login.html', statuses = statuses)
    elif authDeckAccess(deck_id) ==3:
        return  render_template('error.html', value = ['Deck not present'])
    elif authDeckAccess(deck_id) ==2:
        return  render_template('error.html', value = ['You are not authenticated'])
    
    deck = requests.get('http://localhost:8080/api/decks/'+str(deck_id))
    deck =deck.json()
    filename = "exports/export"+str(deck_id)+".csv"
    with open(filename, 'w') as f:
        f.write('Deck ID'+','+ str(deck.get('deck_id'))+"\n")
        f.write('User ID'+','+ str(deck.get('user_id'))+"\n")
        f.write('Deck Name'+','+ str(deck.get('deck_name'))+"\n")
        f.write('Total Score'+','+ str(deck.get('total_score'))+"\n")
        f.write('Cards'+"\n")
        f.write('Card ID, Front, Back, Card Score'+"\n")
        for card in deck.get('cards'):
            f.write(str(card.get('card_id'))+','+str(card.get('front'))+','+str(card.get('back'))+','+str(card.get('card_score'))+"\n")


    return  redirect('/dashboard')
    


@app.route("/cards/add/<int:deck_id>", methods=['GET', 'POST'])
def cardAdd(deck_id):
    if request.method =='GET':
        return  render_template('addcard.html', did = deck_id)
    else:
        values = request.form
        f = values.get('front')
        b = values.get('back')
        did = values.get('deck_id')
        resp = requests.post('http://localhost:8080/api/cards', json={'deck_id':did, 'front':f, 'back':b})
        return  redirect('/decks/'+str(deck_id))



@app.route("/cards/delete/<int:card_id>", methods=['GET', 'POST'])
def cardDelete(card_id):
    card = Cards.query.get(card_id)
    resp = requests.delete('http://localhost:8080/api/cards/'+str(card_id))
    return  redirect('/decks/'+str(card.deck_id))

@app.route("/cards/edit/<int:card_id>", methods=['GET', 'POST'])
def cardEdit(card_id):
    if request.method =='GET':
        card = Cards.query.get(card_id)
        return  render_template('editcard.html', f=card.front, b = card.back, cid = card_id )
    else:
        values = request.form
        f = values.get('front')
        b = values.get('back')
        card = Cards.query.get(card_id)
        resp = requests.put('http://localhost:8080/api/cards/'+str(card_id), json={'front':f, 'back':b })
        return  redirect('/decks/'+str(card.deck_id))



