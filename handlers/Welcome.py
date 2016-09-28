from BlogHandler import BlogHandler
from models import *
from globalstuff import myglobals

class Welcome(BlogHandler):
    ''' This renders a welcome page when new users sign up '''
    def get(self):
        cookie_user_id = None
        if self.request.cookies.get('user_id'):
            cookie_user_id = long(
                            self.request.cookies.get('user_id').split('|')[0])
        if cookie_user_id:
            name = User.by_id(cookie_user_id).name
            print name
            self.render('welcome.html', username=name)
        else:
            self.redirect('/signup')
