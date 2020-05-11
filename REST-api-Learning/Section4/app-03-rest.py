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

# Resource 1
class Item(Resource):
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None) 
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'Message': "An item with name '{}' already exists.".format(name)}, 400
            
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def put(self, name):
        data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

# Resource 2
class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == "__main__":
    app.run(port = 5000, debug = True)