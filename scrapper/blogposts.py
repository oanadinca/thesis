class Post:
    def __init__(self, headline, summary, comments):
        self.headline = headline
        self.summary = summary
        self.comments = comments

    def __repr__(self):
        return '<Post headline= {} summary= {} comments= {}>' \
            .format(self.headline, self.summary, self.comments.__repr__())



class Comment:
    def __init__(self, id, refid, date, user, msg):
        self.id = id
        self.refid = refid
        self.date = date
        self.user = user
        self.msg = msg

    def __repr__(self):
        return '<Comment id= {} refid= {} date= {} user= {} msg= {}>' \
            .format(self.id, self.refid, self.date, self.user, self.msg)
