import uuid
from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView


from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint('Items', __name__)

@blp.route('/item/<string:item_id>')
class Item(MethodView):
    @blp.response(200, ItemSchema) # Genera una respuesta  200 y cualquier cosa que se retorne pasara por el esquema ItemSchema (verificando las condiciones del esquema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found")
    
    # No se necesita un decorador y esquema para la respuesta, ya que solo se retorna un mensaje
    def delete(self, item_id):
        try:
            del items[item_id]
            return {'message': "Item deleted"}
        except KeyError:
            abort(404, message="Item not found")
            
    @blp.arguments(ItemUpdateSchema) # los argumentos de entrada pasaran por el esquema ItemUpdateSchema
    @blp.response(200, ItemSchema) # Genera una respuesta  200 y cualquier cosa que se retorne pasara por el esquema ItemSchema (verificando las condiciones del esquema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data # operador nuevo que sustituye a item.update(item_data)
            return item
        except KeyError:
            abort(404, message="Item not found")
            
@blp.route('/item')
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):             
        for item in items.values():
            if item['name'] == item_data['name'] and item['store_id'] == item_data['store_id']:
                abort(400, message="Item already exists")
                        
        item_id = uuid.uuid4().hex
        item = {**item_data, 'id': item_id}
        items[item_id] = item
        return item


""" ANTES DE APLICAR FILTROS DE MARSHMALLOW
import uuid
from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from db import items

blp = Blueprint('Items', __name__)

@blp.route('/item/<string:item_id>')
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found")
    
    def delete(self, item_id):
        try:
            del items[item_id]
            return {'message': "Item deleted"}
        except KeyError:
            abort(404, message="Item not found")
    
    def put(self, item_id):
        item_data = request.get_json()
        
        if 'name' not in item_data and 'price' not in item_data:
            abort(
                400,
                message="Bad Request. Ensure 'price' and 'name' are provided in the JSON payload"
            )
        
        try:
            item = items[item_id]
            item |= item_data # operador nuevo que sustituye a item.update(item_data)
            return item
        except KeyError:
            abort(404, message="Item not found")
            
@blp.route('/item')
class ItemList(MethodView):
    def get(self):
        return {'items': list(items.values())}
    
    def post(self):
        item_data = request.get_json()
        if (
            'name' not in item_data or
            'price' not in item_data or
            'store_id' not in item_data
        ):
            abort(
                400,
                message="Bad Request. Ensure 'price', 'store_id' and 'name' are provided in the JSON payload" 
            )

        for item in items.values():
            if item['name'] == item_data['name'] and item['store_id'] == item_data['store_id']:
                abort(400, message="Item already exists")
                        
        item_id = uuid.uuid4().hex
        item = {**item_data, 'id': item_id}
        items[item_id] = item
        return item, 201
""" 