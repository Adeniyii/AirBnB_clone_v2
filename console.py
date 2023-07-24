#!/usr/bin/python3
""" Console Module """
import cmd
import sys
import re
import json
import uuid
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }
    FLAG_END_MANY = "end-many"

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        if line.find("+") >= 0:
            commands = line.split(" + ")
            for cmd in commands:
                self.onecmd(cmd)
            return type(self).FLAG_END_MANY
        else:
            kwargs_pattern = re.compile(r'(\w*)=(\"?[a-z0-9A-Z_.@\"-]*)\"?',
                                        re.MULTILINE)
            line_segments = line.split(" ", 2)

            matched_kwargs = kwargs_pattern.findall(line)

            if matched_kwargs and line_segments[0] == "create":
                args_dict = {}

                for v in matched_kwargs:
                    if v[1].find("\"") >= 0:
                        args_dict[v[0]] = v[1].strip("\"").replace("_", " ")
                    elif re.search(r'-?\d*\.\d*', v[1]):
                        args_dict[v[0]] = float(v[1])
                    elif re.search(r'-?\d*', v[1]):
                        args_dict[v[0]] = int(v[1])
                    else:
                        args_dict[v[0]] = v[1].strip("\"").replace("_", " ")

                str_dict = json.dumps(args_dict)
                return "{} {} {}".format(
                    line_segments[0], line_segments[1], str_dict)

            # checks if a dot command `<class>.<command>()` was not used
            if not ('.' in line and '(' in line and ')' in line):
                return line

            try:
                line = self.handle_dot_usage(line)
            except Exception:
                pass
            finally:
                return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def default(self, line):
        """Handle unknown commands"""
        if line == type(self).FLAG_END_MANY:
            return
        cmd.Cmd.default(self, line)

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        parsed_obj = {}
        arg_list = args.split(" ", 1)

        if len(arg_list) > 1:
            try:
                parsed_obj = json.loads(arg_list[1])
                parsed_obj['id'] = str(uuid.uuid4())
            except (json.decoder.JSONDecodeError) as err:
                print("json errrrrrrr")
                return
        else:
            if not arg_list[0]:
                print("** class name missing **")
                return
            elif arg_list[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return

        new_instance = HBNBCommand.classes[arg_list[0]](**parsed_obj)
        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del storage.all()[key]
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            i = 1
            storage_items = storage.all(args).items()
            print("[", end="")
            for _, v in storage_items:
                if '_sa_instance_state' in v.__dict__:
                    del v.__dict__['_sa_instance_state']

                print("[{}] ({}) ".format(v.to_dict()['__class__'], v.id),
                      end="")
                if (len(storage_items) == i):
                    print("{}".format(v.__dict__), end="")
                else:
                    print("{}, ".format(v.__dict__), end="")

                i += 1

            print("]")

        else:
            i = 1
            storage_items = storage.all().items()
            print("[", end="")
            for _, v in storage_items:
                if '_sa_instance_state' in v.__dict__:
                    del v.__dict__['_sa_instance_state']

                print("[{}] ({}) ".format(v.to_dict()['__class__'], v.id),
                      end="")
                if (len(storage_items) == i):
                    print("{}".format(v.__dict__), end="")
                else:
                    print("{}, ".format(v.__dict__), end="")

                i += 1

            print("]")

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        c_name = c_id = att_name = att_val = kwargs = ''

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # isolate args
            args = args[2]
            if args and args[0] == '\"':  # check for quoted arg
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # if att_name was not quoted arg
            if not att_name and args[0] != ' ':
                att_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] == '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            # if att_val was not quoted arg
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for i, att_name in enumerate(args):
            # block only runs on even iterations
            if (i % 2 == 0):
                att_val = args[i + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                # update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")

    @staticmethod
    def parse_command(pline: str):
        return pline[pline.find('.') + 1:pline.find('(')]

    @staticmethod
    def extract_args(pline: str):
        return pline[pline.find('(') + 1:pline.find(')')]

    def handle_dot_usage(self, line):
        _cmd = _cls = _id = _args = ''  # initialize line elements
        # isolate <class name>
        _cls = line[:line.find('.')]

        _cmd = self.parse_command(line)

        if _cmd not in HBNBCommand.dot_cmds:
            raise Exception

        line = self.extract_args(line)

        if line:
            # partition args: (<id>, [<delim>], [<*args>])
            line = line.partition(', ')  # pline convert to tuple

            # isolate _id, stripping quotes
            _id = line[0].replace('\"', '')
            # possible bug here:
            # empty quotes register as empty _id when replaced

            # if arguments exist beyond _id
            line = line[2].strip()  # pline is now str

            if line:
                # check for *args or **kwargs
                if line[0] == '{' and line[-1] == '}'\
                        and type(eval(line)) is dict:
                    _args = line
                else:
                    _args = line.replace(',', '')
                    # _args = _args.replace('\"', '')
        line = ' '.join([_cmd, _cls, _id, _args])

        return line


if __name__ == "__main__":
    HBNBCommand().cmdloop()
