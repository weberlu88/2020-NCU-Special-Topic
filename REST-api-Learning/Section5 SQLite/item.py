import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

# Resource 1
class Item(Resource):

    # No self.parser >> parser is belongs to Class ITSELF.
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
    
    @classmethod
    def create_item(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        result = cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()
        return 

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name) # Item. is okey
        if item:
            return item
        return {'message': 'Item not found'}, 404
        
    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {'Message': "An item with name '{}' already exists.".format(name)}, 400
            
        # filter 'price' go through only . Ignore others.
        data = Item.parser.parse_args() 
        item = {'name': name, 'price': data['price']}
        self.create_item(item)
        return item, 201

    @jwt_required()
    def put(self, name):
        data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

# Resource 2
class ItemList(Resource):
    def get(self):
        return {'items': items}