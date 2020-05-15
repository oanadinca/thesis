from json import JSONEncoder


class Post:
    def __init__(self, id, headline, summary, timestamp, author, url, comments):
        self.id = id
        self.headline = headline
        self.summary = summary
        self.timestamp = str(timestamp)
        self.author = author
        self.url = url
        self.comments = comments

    def __repr__(self):
        return str(self.to_json())

    def to_json(self):
        return {'id': self.id,
                'headline': self.headline,
                'summary': self.summary,
                'timestamp': self.timestamp,
                'author': self.author,
                'url': self.url,
                'comments': self.comments.__repr__()}


class Comment:
    def __init__(self, genid, ref, time, nickname, replied_to, text):
        self.genid = genid
        self.ref = ref
        self.time = str(time)
        self.nickname = nickname
        # self.replied_to = replied_to
        self.text = text

    def __repr__(self):
        return str(self.to_json())

    def to_json(self):
        return {'genid': self.genid,
                'ref': self.ref,
                'time': self.time,
                'nickname': self.nickname,
                # 'replied_to': self.replied_to,
                'text': self.text}


class Contribution:
    def __init__(self, id, conversation):
        self.id = id
        self.conversation = conversation

    def __repr__(self):
        return str(self.to_json())

    def to_json(self):
        return {'id': self.id,
                'conversation': self.conversation.__repr__()}


class PostEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def convert_to_dict(obj):
    """
    A function takes in a custom object and returns a dictionary representation of the object.
    This dict representation includes meta data such as the object's module and class names.
    """

    #  Populate the dictionary with object meta data
    obj_dict = {
        # "__class__": obj.__class__.__name__,
        # "__module__": obj.__module__
    }

    #  Populate the dictionary with object properties
    obj_dict.update(obj.__dict__)

    return obj_dict


def dict_to_obj(our_dict):
    """
    Function that takes in a dict and returns a custom object associated with the dict.
    This function makes use of the "__module__" and "__class__" metadata in the dictionary
    to know which object type to create.
    """
    if "__class__" in our_dict:
        # Pop ensures we remove metadata from the dict to leave only the instance arguments
        class_name = our_dict.pop("__class__")

        # Get the module name from the dict and import it
        module_name = our_dict.pop("__module__")

        # We use the built in __import__ function since the module name is not yet known at runtime
        module = __import__(module_name)

        # Get the class from the module
        class_ = getattr(module, class_name)

        # Use dictionary unpacking to initialize the object
        obj = class_(**our_dict)
    else:
        obj = our_dict
    return obj
