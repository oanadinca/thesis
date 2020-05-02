class Post:
    def __init__(self, id, headline, summary, url, comments):
        self.id = id
        self.headline = headline
        self.summary = summary
        self.url = url
        self.comments = comments

    def __repr__(self):
        return '<Post id= {} headline= {} summary= {} url={} comments= {}>' \
            .format(self.id, self.headline, self.summary, self.url, self.comments.__repr__())


class Comment:
    def __init__(self, id, ref_id, timestamp, username, replied_to, msg):
        self.id = id
        self.ref_id = ref_id
        self.timestamp = timestamp
        self.username = username
        self.replied_to = replied_to
        self.msg = msg

    def __repr__(self):
        return '<Comment id= {} ref_id= {}>' \
            .format(self.id, self.ref_id)
