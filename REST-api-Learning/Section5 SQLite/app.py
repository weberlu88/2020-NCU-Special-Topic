from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'iwanna8som7pancake'
api = Api(app)

# Auth with User id
jwt = JWT(app, authenticate, identity)

# /auth is auto create by 'jwt = JWT(app, authenticate, identity)' https://blog.tecladocode.com/simple-jwt-authentication-with-flask-jwt/
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    app.run(port = 5000, debug = True)