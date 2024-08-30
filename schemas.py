from marshmallow import Schema, fields

class ItemSchema(Schema):
    id = fields.Str(dump_only=True)  # puede ser usado cargar data desde una request o para devolver data en una response del API
    name = fields.Str(required=True) # required=True significa que este campo es obligatorio
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)
    
class ItemUpdateSchema(Schema):
    # aqui no se requiere que los campos sean obligatorios
    name = fields.Str()
    price = fields.Float()
    
class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)