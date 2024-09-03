import os
import secrets

from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db

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
    app.config['JWT_SECRET_KEY'] = secrets.SystemRandom().getrandbits(128) # Esta clave sirve para firmar los tokens
    #app.config['JWT_SECRET_KEY'] = "supercalifragilisticoespialidoso"
    
    db.init_app(app)
    api = Api(app)


    with app.app_context():
        db.create_all()

    jwt = JWTManager(app)

    # Registrando los blueprints
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
