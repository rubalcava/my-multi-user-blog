from BlogHandler import BlogHandler
from models import *
from globalstuff import myglobals

class MainPage(BlogHandler):
    ''' This routes to main blog page '''
    def get(self):
        self.redirect('/blog')
