from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
import secrets   

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

app = Flask(__name__)

# Configuracion de la app
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['API_TITLE'] = "Stores REST API"
app.config['API_VERSION'] = "v1"
app.config['OPENAPI_VERSION'] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = "/"
app.config['OPENAPI_SWAGGER_UI_PATH'] = "/swagger-ui"
app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

app.config['JWT_SECRET_KEY'] = "supercalifragilisticoespialidoso"
#app.config['JWT_SECRET_KEY'] = secrets.SystemRandom().getrandbits(128)
jwt = JWTManager(app)

# Registrando los blueprints
api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)

if __name__ == '__main__':
    app.run(debug=True)


""" APUNTES
    recibiendo por operador ? en la url query string params
    recibiendo por header
    recibiendo info por url (como el decorador de  create_item)
    
    
    ****EL SIGUIENTE CODIGO ES SIN BLUEPRINTS****
    
import uuid
from flask import Flask, request, abort
from db import items, stores

# ****************************************************
# get-all-stores
@app.get('/store')
def get_stores():
    return {'stores': list(stores.values())}

# ****************************************************
# create-store
@app.post('/store')
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400, message="Bad Request. Ensure 'name' is included in the JSON payload")
    
    for store in stores.values():
        if store_data['name'] == store['name']:
            abort(400, message="Store already exists")
                
    store_id = uuid.uuid4().hex
    store = {**store_data, 'id': store_id}
    stores[store_id] = store
    return store, 201

# ****************************************************
# create-item
@app.post('/item') 
def create_item():
    item_data = request.get_json()
    # Comprobando si el json tiene los campos necesarios
    if (
        'name' not in item_data or
        'price' not in item_data or
        'store_id' not in item_data
    ):
        # abort es una funcion de flask que permite retornar un error con un mensaje
        abort(
            400,
            message="Bad Request. Ensure 'price', 'store_id' and 'name' are provided in the JSON payload" 
        )
    
    # Comprobando si el la dupla name-store_id ya existe
    for item in items.values():
        if item['name'] == item_data['name'] and item['store_id'] == item_data['store_id']:
            abort(400, message="Item already exists")
            
    '''Reescribiendo el codigo anterior para que se vea distinto, "mas legible"
    # Comprobando si el la dupla name-store_id ya existe
    for item in items.values():
        if (
            item_data['name'] == item['name']
            and item_data['store_id'] == item['store_id'] 
        ):
            abort(
                400,
                message="Item already exists"
            )
    
    '''
    
    if item_data['store_id'] not in stores:
        abort(404, message="Store not found")
    
    item_id = uuid.uuid4().hex
    item = {**item_data, 'id': item_id}
    items[item_id] = item
    return item, 201

# ****************************************************
# get-all-items
@app.get('/item')
def get_all_items():
    return {'items': list(items.values())}

# ****************************************************
# get-one-store
@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found")

# ****************************************************    
# get-one-item
@app.get('/item/<string:item_id>') 
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found")

# ****************************************************    
# delete-item
@app.delete('/item/<string:item_id>')
def delete_item(item_id):
    try:
        del items[item_id]
        return {'message': "Item deleted"}
    except KeyError:
        abort(404, message="Item not found")

# ****************************************************    
# update-item
@app.put('/item/<string:item_id>')
def update_item(item_id):
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

# ****************************************************    
# delete-store
@app.delete('/store/<string:store_id>')
def delete_store(store_id):
    try:
        del stores[store_id]
        return {'message': "Store deleted"}
    except KeyError:
        abort(404, message="Store not found")



if __name__ == '__main__':
    app.run(debug=True)
    
"""