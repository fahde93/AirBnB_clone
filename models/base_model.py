#!/usr/bin/python3
"""Defines BaseModel class."""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Represents BaseModel of the HBnB project."""

    def __init__(self, *args, **kwargs):
        """Initialize new BaseModel.

        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs attributes.
        """
        ftform = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = (str(uuid4()))
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for f, s in kwargs.items():
                if f == "created_at" or f == "updated_at":
                    self.__dict__[f] = datetime.strptime(s, ftform)
                else:
                    self.__dict__[f] = s
        else:
            models.storage.new(self)

    def save(self):
        """Update updated_at with current datetime."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Return dictionary of baseModel instance.

        Includes the key/value pair __class__ representing
        the class name the object.
        """
        fdict = self.__dict__.copy()
        fdict["created_at"] = self.created_at.isoformat()
        fdict["updated_at"] = self.updated_at.isoformat()
        fdict["__class__"] = self.__class__.__name__
        return fdict

    def __str__(self):
        """Return the print/str representation of BaseModel instance."""
        flname = self.__class__.__name__
        return "[{}] ({}) {}".format(flname, self.id, self.__dict__)
