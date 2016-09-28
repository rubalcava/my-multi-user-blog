from Signup import Signup
from models import *
from globalstuff import myglobals

class Register(Signup):
    ''' This is how a new user is added to the db '''
    def done(self):
        # override Signup class's done function to ensure
        # user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username=msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/welcome')
