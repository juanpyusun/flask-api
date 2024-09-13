import os
import secrets

from flask import Flask, jsonify  # jsonify es una función que convierte un diccionario en un JSON
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db

from blocklist import BLOCKLIST
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

# Factory para crear la app
def create_app(db_url=None):    
    app = Flask(__name__)

    # Configuracion de la app
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = "Stores REST API"
    app.config['API_VERSION'] = "v1"
    app.config['OPENAPI_VERSION'] = "3.0.3"
    app.config['OPENAPI_URL_PREFIX'] = "/"
    app.config['OPENAPI_SWAGGER_UI_PATH'] = "/swagger-ui"
    app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv('DATABASE_URL', 'sqlite:///data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = str(secrets.SystemRandom().getrandbits(128)) # Esta clave sirve para firmar los tokens
    #app.config['JWT_SECRET_KEY'] = "supercalifragilisticoespialidoso"
    
    db.init_app(app)
    api = Api(app)

    # Esta es una forma de crear la base de datos si no existe al iniciar la app
    with app.app_context():
        db.create_all()

    # Inicializando el JWTManager
    jwt = JWTManager(app)
    
    # Función para verificar si un token está en la lista negra
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (jsonify({"description": "The token has been revoked.", "error": "token_revoked"}), 401)

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (jsonify({"description": "The token is not fresh.", "error": "fresh_token_required",}), 401)
        
    # Función para obtener el identificador del usuario
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity): # Recordemos que el identity es el id del usuario que viene encapsulado en el token
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}
        
    # Funciones para manejar errores de autenticación
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (jsonify({"message": "The token has expired.", "error": "token_expired"}), 401)

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401)

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (jsonify({"description": "Request does not contain an access token.", "error": "authorization_required",}), 401)


    # Registrando los blueprints
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
