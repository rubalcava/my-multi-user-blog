from google.appengine.ext import db
from globalstuff import myglobals

class User(db.Model):
    ''' This defines users for storage in the db '''
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()
    liked_posts = db.StringListProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=myglobals.users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = myglobals.make_pw_hash(name, pw)
        return User(parent=myglobals.users_key(),
                    name=name,
                    pw_hash=pw_hash,
                    email=email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and myglobals.valid_pw(name, pw, u.pw_hash):
            return u
