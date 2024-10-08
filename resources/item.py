from flask_smorest import abort, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint('Items', __name__)

@blp.route('/item/<int:item_id>')
class Item(MethodView):
    @jwt_required() # Se agrega en cada método que requiera autenticación
    @blp.response(200, ItemSchema) # Genera una respuesta  200 y cualquier cosa que se retorne pasara por el esquema ItemSchema (verificando las condiciones del esquema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    # No se necesita un decorador y esquema para la respuesta, ya que solo se retorna un mensaje
    @jwt_required()
    def delete(self, item_id):
        # Este bloque de código verifica si el usuario es administrador
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
            
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted successfully"}
        
    @jwt_required()    
    @blp.arguments(ItemUpdateSchema) # los argumentos de entrada pasaran por el esquema ItemUpdateSchema
    @blp.response(200, ItemSchema) # Genera una respuesta  200 y cualquier cosa que se retorne pasara por el esquema ItemSchema (verificando las condiciones del esquema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data['price']
            item.name = item_data['name']
        else:
            item = ItemModel(id=item_id, **item_data)
        
        db.session.add(item)
        db.session.commit()
        #raise NotImplementedError("Updating method not implemented") # raise NotImplementedError es una excepción que se usa para indicar que un método no ha sido implementado durante el desarrollo
        return item

@blp.route('/item')
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    
    @jwt_required(fresh=True) # Con fresh=True, se requiere que el token sea fresco, es decir, que haya sido emitido por el servidor
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error ocurred creating the item")
        return item
