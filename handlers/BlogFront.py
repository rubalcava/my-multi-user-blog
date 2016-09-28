from models import *
from BlogHandler import BlogHandler
from globalstuff import myglobals

class BlogFront(BlogHandler):
    ''' This is how posts are grabbed from the db and rendered on screen '''
    def get(self):
        posts = greetings = Post.all().order('-created')
        comments = Comment.all().order('-created')
        self.render('front.html', posts=posts, comments=comments)
