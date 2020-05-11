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

# Resource 1. 
class Item(Resource):
    def get(self, name):
        # find item with name. next() get 1st elem in filter. item may be None/object (default None).
        item = next(filter(lambda x: x['name'] == name, items), None) 
        return {'item': item}, 200 if item else 404
    
    def post(self, name):
        # if item already exists, failed (400 bad request)
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'Message': "An item with name '{}' already exists.".format(name)}, 400
            
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