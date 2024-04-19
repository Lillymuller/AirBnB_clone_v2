#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is not None:
            if isinstance(cls, str):
                cls = eval(cls)
            store = self.__objects.items()
            dicts = {key: val for key, val in store if instance(val, cls)}
            return dicts

        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r', encoding="utf-8") as f:
                data = json.load(f)
                for obj_data in data.values():
                    obj_class = obj_data["__class__"]
                    del obj_data["__class__"]
                    obj_instance = eval(obj_class)(**obj_data)
                    self.new(obj_instance)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """ Delete the object from __object"""
        if obj is not None:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects.pop(key, None)

    def close(self):
        """call reload() method for deserializing the JSON file to objects """
        self.reload()
