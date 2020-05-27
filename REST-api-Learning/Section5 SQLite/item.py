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
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()
        return 
    
    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()
        return

    @classmethod
    def delete_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE from items WHERE name=?"
        cursor.execute(query, (name,))

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
        '''Create a new item.'''
        if self.find_by_name(name):
            return {'Message': "An item with name '{}' already exists.".format(name)}, 400
            
        # filter 'price' go through only . Ignore others.
        data = Item.parser.parse_args() 
        item = {'name': name, 'price': data['price']}
        try:
            self.insert(item)
        except:
            return {"message": "An error occurred inserting the item."}, 500 # internal server error
        return item, 201

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occurred inserting the item."}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occurred updating the item."}, 500
        return updated_item

    @jwt_required()
    def delete(self, name):
        try:
            item = self.find_by_name(name)
            if item:
                self.delete_by_name(name)
            else:
                return {'message': 'Item not found'}
        except:
            return {"message": "An error occurred deleting the item."}, 500
        return {'message': 'Item deleted'}

# Resource 2
class ItemList(Resource):
    TABLE_NAME = 'items'

    @classmethod
    def get_all(cls):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=cls.TABLE_NAME)
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()

        return items

    def get(self):
        try:
            items = ItemList.get_all()
        except:
            return {"message": "An error occurred getting all items."}, 500 # internal server error
        return {'items': items}