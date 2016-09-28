from BlogHandler import BlogHandler
from models import *
from globalstuff import myglobals
from google.appengine.ext import db

class EditPost(BlogHandler):
    ''' This is the edit post page that handles edits and deletions '''
    def get(self, post_id):
        if self.user:
            # look up the post by id and get its stuff to populate form
            gql_lookup = Post.gql("WHERE post_id = :post_id",
                                  post_id=post_id)
            looked_up_post = gql_lookup.get()

            subject = looked_up_post.subject
            content = looked_up_post.content
            post_link = "/blog/" + post_id
            if str(self.user.key().id()) == looked_up_post.user_id:
                self.render("editpost.html", post_id=post_id, subject=subject,
                            content=content, post_link=post_link)
            else:
                self.render("notyours.html")
        else:
            self.redirect("/login")

    def post(self, post_id):
        if self.user:
            # look up post to verify if user is author
            gql_lookup = Post.gql("WHERE post_id = :post_id", post_id=post_id)
            looked_up_post = gql_lookup.get()
            current_user_id = str(self.user.key().id())
            author_user_id = str(looked_up_post.user_id)

            if current_user_id == author_user_id:
                subject = self.request.get('subject')
                content = self.request.get('content')
                delete_checked = self.request.get('delete-checkbox')

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
                        self.render("editpost.html", post_id=post_id,
                                    subject=subject, content=content, error=error)
            else:
                self.render("notyours.html")
        else:
            self.redirect("/login")
