# con esto se importan todos los modelos de la carpeta models, asi al llamarlos en los recursos no se necesita importarlos uno por uno
from models.store import StoreModel
from models.item import ItemModel
from models.tag import TagModel
from models.item_tags import ItemTags
from models.user import UserModel
