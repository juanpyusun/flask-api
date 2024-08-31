from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship("ItemModel", back_populates="store", lazy='dynamic', cascade="all, delete")
    # lazy='dynamic' significa que no se cargaran los items de la tienda a menos que se llame a la propiedad items
    # cascade="all, delete" significa que si se elimina una tienda, se eliminaran todos los items asociados a ella
