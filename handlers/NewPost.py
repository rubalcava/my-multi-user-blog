from google.appengine.ext import db
from BlogHandler import BlogHandler
from models import *
from globalstuff import myglobals

class NewPost(BlogHandler):
    ''' This is the new post page that handles new submissions '''
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        if self.user:
            subject = self.request.get('subject')
            content = self.request.get('content')

            user_id = str(self.user.key().id())
            username = str(self.user.name)

            if subject and content:
                p = Post(parent=myglobals.blog_key(), subject=subject, content=content,
                         user_id=user_id, username=username, likes=0)

                p_key = p.put()
                p_returned = db.get(p_key)
                p_returned.post_id = str(p_key.id())
                p_returned.post_key = str(p_key)
                p_returned.put()

                self.redirect('/blog/%s' % str(p.key().id()))
            else:
                error = "subject and content, please!"
                self.render("newpost.html", subject=subject,
                            content=content, error=error)
        else:
            self.redirect('/login')
