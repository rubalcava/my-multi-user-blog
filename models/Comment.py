from google.appengine.ext import db
from globalstuff import myglobals

class Comment(db.Model):
    ''' This is how comments are defined for storage in the db '''
    author_name = db.StringProperty(required=True)
    author_id = db.StringProperty(required=True)
    post_id = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    content = db.TextProperty(required=True)
    comment_id = db.StringProperty(required=False)
    comment_key = db.StringProperty(required=False)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return myglobals.render_str("comment.html", c=self)
