from BlogHandler import BlogHandler
from models import *
from globalstuff import myglobals

class Logout(BlogHandler):
    ''' This defines how users logout '''
    def get(self):
        self.logout()
        self.redirect('/signup')
