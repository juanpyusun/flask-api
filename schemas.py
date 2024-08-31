from marshmallow import Schema, fields

# Esta clase es de ItemSchema, excluyendo la información de la relación con StoreModel
class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)  # puede ser usado cargar data desde una request o para devolver data en una response del API
    name = fields.Str(required=True) # required=True significa que este campo es obligatorio
    price = fields.Float(required=True)

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    
class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True) # atributo nested se usa para anidar un schema dentro de otro
    store = fields.Nested(PlainStoreSchema(), dump_only=True) # dump_only=True significa que este campo no se puede cargar desde una request
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)
    
class ItemUpdateSchema(Schema):
    # aqui no se requiere que los campos sean obligatorios
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()
    
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)
    
class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    
class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)
    
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True) #load_only=True significa que este campo no se puede devolver en una response