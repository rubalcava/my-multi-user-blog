import os
import re
import random
import hashlib
import hmac
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

from handlers import *

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/welcome', Welcome),
                               ('/blog', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/blog/edit/([0-9]+)', EditPost),
                               ('/blog/deleted', Deleted),
                               ('/blog/like/([0-9]+)', LikePost),
                               ('/blog/comment/add/([0-9]+)', NewComment),
                               ('/blog/comment/edit/([0-9]+)', EditComment)
                               ],
                              debug=True)
