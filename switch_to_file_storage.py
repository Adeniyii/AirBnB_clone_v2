#!/usr/bin/python3
from models.base_model import BaseModel


class Base():
    pass


from models.user import User  # noqa
from models.amenity import Amenity  # noqa
from models.city import City  # noqa
from models.place import Place  # noqa
from models.state import State  # noqa
from models.review import Review  # noqa
from models.engine import file_storage  # noqa


storage = file_storage.FileStorage()
storage.reload()
