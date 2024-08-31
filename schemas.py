from marshmallow import Schema, fields

# Esta clase es de ItemSchema, excluyendo la información de la relación con StoreModel
class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)  # puede ser usado cargar data desde una request o para devolver data en una response del API
    name = fields.Str(required=True) # required=True significa que este campo es obligatorio
    price = fields.Float(required=True)

class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    
class ItemUpdateSchema(Schema):
    # aqui no se requiere que los campos sean obligatorios
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True) # atributo nested se usa para anidar un schema dentro de otro
    store = fields.Nested(PlainStoreSchema(), dump_only=True) # dump_only=True significa que este campo no se puede cargar desde una request
    
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)