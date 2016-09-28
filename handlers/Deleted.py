from BlogHandler import BlogHandler
from models import *
from globalstuff import myglobals

class Deleted(BlogHandler):
    def get(self):
        self.render("deleted.html")
