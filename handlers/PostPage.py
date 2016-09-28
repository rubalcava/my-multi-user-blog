from google.appengine.ext import db
from BlogHandler import BlogHandler
from models import *
from globalstuff import myglobals

class PostPage(BlogHandler):
    ''' This is how permalink pages for individual posts are rendered '''
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=myglobals.blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        comments = Comment.all().order('-created')

        self.render("permalink.html", post=post, comments=comments)
