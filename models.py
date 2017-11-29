from openviz import db

class Catalan(db.Model):

    __tablename__ = "catalan"
    #__bind_key__ = "ca"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.UnicodeText(64))
    vector = db.Column(db.Text)


class Url():
    id = 0
    url = ""
    freqs = ""
    title = ""
    vector = None
    snippet = ""


    def __init__(self, id=None, url=None, freqs=None, title=None, vector=None, snippet=None):
        self.id = id
        self.url = url
        self.freqs = freqs
        self.title = title
        self.vector = vector
        self.snippet = snippet

    def __repr__(self):
       return self.url

