#!/usr/bin/python3
"""the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    fcurly_braces = re.search(r"\{(.*?)\}", arg)
    fbrackets = re.search(r"\[(.*?)\]", arg)
    if fcurly_braces is None:
        if fbrackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            flexer = split(arg[:fbrackets.span()[0]])
            fretl = [i.strip(",") for i in flexer]
            fretl.append(fbrackets.group())
            return fretl
    else:
        flexer = split(arg[:fcurly_braces.span()[0]])
        fretl = [i.strip(",") for i in flexer]
        fretl.append(fcurly_braces.group())
        return fretl


class HBNBCommand(cmd.Cmd):
    """Defines the alxbnb command interpreter.
    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        fargdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        fmatch = re.search(r"\.", arg)
        if fmatch is not None:
            fargl = [arg[:fmatch.span()[0]], arg[fmatch.span()[1]:]]
            fmatch = re.search(r"\((.*?)\)", fargl[1])
            if fmatch is not None:
                fcommand = [fargl[1][:fmatch.span()[0]], fmatch.group()[1:-1]]
                if fcommand[0] in fargdict.keys():
                    ycall = "{} {}".format(fargl[0], fcommand[1])
                    return fargdict[fcommand[0]](ycall)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        fargl = parse(arg)
        if len(fargl) == 0:
            print("** class name missing **")
        elif fargl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(fargl[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        fargl = parse(arg)
        fobjdict = storage.all()
        if len(fargl) == 0:
            print("** class name missing **")
        elif fargl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(fargl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(fargl[0], fargl[1]) not in fobjdict:
            print("** no instance found **")
        else:
            print(fobjdict["{}.{}".format(fargl[0], fargl[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        fargl = parse(arg)
        fobjdict = storage.all()
        if len(fargl) == 0:
            print("** class name missing **")
        elif fargl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(fargl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(fargl[0], fargl[1]) not in fobjdict.keys():
            print("** no instance found **")
        else:
            del fobjdict["{}.{}".format(fargl[0], fargl[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        fargl = parse(arg)
        if len(fargl) > 0 and fargl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            fobjl = []
            for obj in storage.all().values():
                if len(fargl) > 0 and fargl[0] == obj.__class__.__name__:
                    fobjl.append(obj.__str__())
                elif len(fargl) == 0:
                    fobjl.append(obj.__str__())
            print(fobjl)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        fargl = parse(arg)
        fcount = 0
        for obj in storage.all().values():
            if fargl[0] == obj.__class__.__name__:
                fcount += 1
        print(fcount)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        fargl = parse(arg)
        fobjdict = storage.all()

        if len(fargl) == 0:
            print("** class name missing **")
            return False
        if fargl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(fargl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(fargl[0], fargl[1]) not in fobjdict.keys():
            print("** no instance found **")
            return False
        if len(fargl) == 2:
            print("** attribute name missing **")
            return False
        if len(fargl) == 3:
            try:
                type(eval(fargl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(fargl) == 4:
            obj = fobjdict["{}.{}".format(fargl[0], fargl[1])]
            if fargl[2] in obj.__class__.__dict__.keys():
                yvaltype = type(obj.__class__.__dict__[fargl[2]])
                obj.__dict__[fargl[2]] = yvaltype(fargl[3])
            else:
                obj.__dict__[fargl[2]] = fargl[3]
        elif type(eval(fargl[2])) == dict:
            obj = fobjdict["{}.{}".format(fargl[0], fargl[1])]
            for k, v in eval(fargl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    yvaltype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = yvaltype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
