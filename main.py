from flask import *
from application.config import *
from flask_restful import Resource
from application.database import * 
dev=True                        # true for development server

def create_app():
    app = Flask(__name__, template_folder='templates')
    if dev:
        print('starting dev server')
        app.config.from_object(LocalDevConfig)
    else:
        print('starting production server')
        app.config.from_object(ProductionConfig)
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()
from application.controllers import *
from application.apiEndpoints import * 


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080, debug = 'True')
    #app.run(host='0.0.0.0',port=8080)