#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls:
            return {k: v for k, v in FileStorage.__objects.items()
                    if v.to_dict()['__class__'] == cls}

        return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        FileStorage.__objects.update(
            {obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            for key, val in FileStorage.__objects.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """delete an object from in-memory storage"""
        if (obj is None):
            return

        key = "{}.{}".format(str(type(obj)).split('.')[-1].split('\'')[0],
                             obj.__dict__.get("id"))

        if key in FileStorage.__objects:
            del FileStorage.__objects[key]

    def cities(self, state_id):
        """return a list of cities with state_id equal to the current State.id
        """
        city_list = []

        for k, v in FileStorage.__objects.items():
            if k.split('.')[-1].split('\'')[0] != 'City':
                continue

            if v.get('state_id') == state_id:
                city_list.append(v)

        return city_list
