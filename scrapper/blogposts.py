class Post:
    def __init__(self, id, headline, summary, comments):
        self.id = id
        self.headline = headline
        self.summary = summary
        self.comments = comments

    def __repr__(self):
        return '<Post id= {} headline= {} summary= {} comments= {}>' \
            .format(self.id, self.headline, self.summary, self.comments.__repr__())


class Comment:
    def __init__(self, id, refid, timestamp, user, msg):
        self.id = id
        self.refid = refid
        self.timestamp = timestamp
        self.user = user
        self.msg = msg

    def __repr__(self):
        return '<Comment id= {} refid= {}>' \
            .format(self.id, self.refid)
