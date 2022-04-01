from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'my_secret_key'
api = Api(app)
jwt = JWT(app, authenticate, identity)
items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True, help="You must not left this field blank!")
    data = parser.parse_args()
    @jwt_required()
    def get(self, name):
        return {'item': next(filter(lambda x: x['name'] == name, items), None)}

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {"message": f"An item with name '{name}' already exists."}
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name']!= name, items))
        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name']==name, items), None)
        if not item:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(port=4000,debug=True)