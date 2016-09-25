import os
import re
import random
import hashlib
import hmac
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

secret = 'kjgdsag'

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

class BlogHandler(webapp2.RequestHandler):
    ''' This class contains helper functions to render the blog and set cookies '''
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

##### Cryptofunctions
def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

def users_key(group = 'default'):
    return db.Key.from_path('users', group)

##### end of Cryptofunctions

class User(db.Model):
    ''' This defines users for storage in the db '''
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u


##### Blog function

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class Post(db.Model):
    ''' This is how posts are defined for storage in the db '''
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    user_id = db.StringProperty(required = True)
    username = db.StringProperty(required = True)
    post_id = db.StringProperty(required = False)
    post_key = db.StringProperty(required = False)
    likes = db.IntegerProperty(required = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)

class BlogFront(BlogHandler):
    ''' This is how posts are grabbed from the db and rendered on screen '''
    def get(self):
        posts = greetings = Post.all().order('-created')
        self.render('front.html', posts = posts)

class PostPage(BlogHandler):
    ''' This is how permalink pages for individual posts are rendered '''
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post = post)

class NewPost(BlogHandler):
    ''' This is the new post page that handles new submissions '''
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        if not self.user:
            self.redirect('/blog')

        subject = self.request.get('subject')
        content = self.request.get('content')

        cookie_user_id = self.request.cookies.get('user_id').split('|')[0]
        username = User.by_id(long(cookie_user_id)).name

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content, user_id = cookie_user_id, username = username, likes = 0)

            p_key = p.put()
            p_returned = db.get(p_key)
            p_returned.post_id = str(p_key.id())
            p_returned.post_key = str(p_key)
            p_returned.put()

            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)

# class no longer used. replaced by edit post link which goes straight to intended post.
#
# class Lookup(BlogHandler):
#     ''' This is the lookup page that checks if a post_id is valid '''
#     def get(self):
#         if self.user:
#             self.render("lookup.html")
#         else:
#             self.redirect("/login")
#
#     def post(self):
#         if not self.user:
#             self.redirect('/blog')
#
#         this_post_id = self.request.get('post_id')
#
#         if self.request.get('post_id').isdigit():
#             # search for the post by the passed in post_id
#             gql_lookup = Post.gql("WHERE post_id = :post_id", post_id=this_post_id)
#             looked_up_post = gql_lookup.get()
#             # if a post was found, post_id is valid
#             if looked_up_post:
#                 self.redirect('/blog/edit/%s' % this_post_id)
#             else:
#                 error = "post not found"
#                 self.render("lookup.html", post_id = this_post_id, error = error)
#         else:
#             error = "invalid format (numbers only)"
#             self.render("lookup.html", post_id = this_post_id, error = error)
#
# end of lookup class

class EditPost(BlogHandler):
    ''' This is the edit post page that handles edits and deletions '''
    def get(self, post_id):
        if self.user:
            # look up the post by id and get its stuff to populate form
            gql_lookup = Post.gql("WHERE post_id = :post_id", post_id=post_id)
            looked_up_post = gql_lookup.get()

            subject = looked_up_post.subject
            content = looked_up_post.content

            self.render("editpost.html", post_id = post_id, subject = subject, content = content)
        else:
            self.redirect("/login")

    def post(self, post_id):
        if not self.user:
            self.redirect('/blog')

        # look up post to verify if logged in user is author
        gql_lookup = Post.gql("WHERE post_id = :post_id", post_id=post_id)
        looked_up_post = gql_lookup.get()
        current_user_id = str(self.user.key().id())
        author_user_id = str(looked_up_post.user_id)

        subject = self.request.get('subject')
        content = self.request.get('content')
        delete_checked = self.request.get('delete-checkbox')

        if current_user_id == author_user_id:
            if delete_checked:
                db.delete(looked_up_post.key())
                self.redirect('/blog/deleted')
            if not delete_checked:
                if subject and content:
                    looked_up_post.subject = subject
                    looked_up_post.content = content
                    looked_up_post.put()
                    self.redirect('/blog/%s' % post_id)
                else:
                    error = "subject and content, please!"
                    self.render("editpost.html", post_id = post_id, subject=subject, content=content, error=error)
        else:
            error = "don't mess with someone else's post!"
            self.render("editpost.html", post_id = post_id, subject=subject, content=content, error=error)

class Deleted(BlogHandler):
    def get(self):
        self.render("deleted.html")

class LikePost(BlogHandler):
    def get(self, post_id):
        # look up post to verify if logged in user is author
        gql_lookup = Post.gql("WHERE post_id = :post_id", post_id=post_id)
        looked_up_post = gql_lookup.get()
        current_user_id = str(self.user.key().id())
        author_user_id = str(looked_up_post.user_id)

        if current_user_id != author_user_id:
            current_likes = looked_up_post.likes
            looked_up_post.likes = current_likes + 1
            looked_up_post.put()
            self.render("permalink.html", post = looked_up_post)
        else:
            error = "can't like your own posts"
            self.render("permalink.html", post = looked_up_post, error = error)

# Form validation functions

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(BlogHandler):
    ''' This is how users sign up '''
    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username = self.username,
                      email = self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError

class Register(Signup):
    ''' This is how a new user is added to the db '''

    def done(self):
        # Override Signup class's done function to ensure user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/welcome')

class Login(BlogHandler):
    ''' This defines how users login '''
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/welcome')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)

class Logout(BlogHandler):
    ''' This defines how users logout '''
    def get(self):
        self.logout()
        self.redirect('/signup')

class MainPage(BlogHandler):
    def get(self):
        self.redirect('/blog')

class Welcome(BlogHandler):
    def get(self):
        cookie_user_id = None
        if self.request.cookies.get('user_id'):
            cookie_user_id = long(self.request.cookies.get('user_id').split('|')[0])
        if cookie_user_id:
            name = User.by_id(cookie_user_id).name
            print name
            self.render('welcome.html', username = name)
        else:
            self.redirect('/signup')


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/welcome', Welcome),
                               ('/blog', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               # ('/blog/lookup', Lookup),
                               ('/blog/edit/([0-9]+)', EditPost),
                               ('/blog/deleted', Deleted),
                               ('/blog/like/([0-9]+)', LikePost)
                               ],
                              debug=True)
