from json import JSONEncoder


class Post:
    def __init__(self, id, headline, summary, timestamp, author, url, comments):
        self.id = id
        self.headline = headline
        self.summary = summary
        self.timestamp = timestamp
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
    def __init__(self, id, ref_id, timestamp, username, replied_to, msg):
        self.id = id
        self.ref_id = ref_id
        self.timestamp = timestamp
        self.username = username
        self.replied_to = replied_to
        self.msg = msg

    def __repr__(self):
        return str(self.to_json())

    def to_json(self):
        return {'id': self.id,
                'ref_id': self.ref_id,
                'timestamp': self.timestamp,
                'username': self.username,
                'replied_to': self.replied_to,
                'msg': self.msg}


class PostEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
