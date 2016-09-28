from google.appengine.ext import db
from globalstuff import myglobals

class Post(db.Model):
    ''' This is how posts are defined for storage in the db '''
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    user_id = db.StringProperty(required=True)
    username = db.StringProperty(required=True)
    post_id = db.StringProperty(required=False)
    post_key = db.StringProperty(required=False)
    likes = db.IntegerProperty(required=True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return myglobals.render_str("post.html", p=self)
