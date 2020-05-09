from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# Data stored in memory
items = [
    {
        'name': 'iphone SE',
        'price': 999.9
    }
]

# Resource 1. A class, each resource may has its own GET POST PUT DEL...
class Item(Resource):
    def get(self, name):
        for i in items:
            if i['name'] == name:
                return i # Default status 200
        return {'item': None}, 404 # Error, item not in list
    
    def post(self, name):
        data = request.get_json(silent = True) # https://flask.palletsprojects.com/en/1.1.x/api/#flask.Request.get_json
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201


# Resource 2
class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port = 5000, debug = True)