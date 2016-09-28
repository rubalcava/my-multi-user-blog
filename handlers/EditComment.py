from BlogHandler import BlogHandler
from models import *
from globalstuff import myglobals
from google.appengine.ext import db

class EditComment(BlogHandler):
    ''' This defines how comments are edited '''
    def get(self, comment_id):
        if self.user:
            # get all comments for later
            comments = Comment.all().order('-created')
            # look up the comment and then get the post its associated with
            gql_comment_lookup = Comment.gql("WHERE comment_id = :comment_id",
                                             comment_id=comment_id)
            looked_up_comment = gql_comment_lookup.get()
            post_id = looked_up_comment.post_id

            gql_post_lookup = Post.gql("WHERE post_id = :post_id",
                                       post_id=post_id)
            looked_up_post = gql_post_lookup.get()

            if str(self.user.key().id()) == looked_up_comment.author_id:
                self.render('editcomment.html', p=looked_up_post,
                            comments=comments, content=looked_up_comment.content)
            else:
                self.render("notyours.html")
        else:
            self.redirect("/login")

    def post(self, comment_id):
        if self.user:
            # get all comments in case they need to be used later
            comments = Comment.all().order('-created')
            # look up comment to verify if signed in user is author
            gql_comment_lookup = Comment.gql("WHERE comment_id = :comment_id",
                                            comment_id=comment_id)
            looked_up_comment = gql_comment_lookup.get()
            post_id = looked_up_comment.post_id
            # look up post in case page needs to be re-rendered later
            gql_post_lookup = Post.gql("WHERE post_id = :post_id", post_id=post_id)
            looked_up_post = gql_post_lookup.get()
            current_user_id = str(self.user.key().id())
            author_user_id = str(looked_up_comment.author_id)

            content = self.request.get('content')
            delete_checked = self.request.get('delete-checkbox')

            if current_user_id == author_user_id:
                if delete_checked:
                    db.delete(looked_up_comment.key())
                    self.redirect('/blog/deleted')
                if not delete_checked:
                    if content:
                        looked_up_comment.content = content
                        # redirect wasn't showing updated comment, so an extra db
                        # get/put is used to ensure it's updated
                        c_key = looked_up_comment.put()
                        c_returned = db.get(c_key)
                        c_returned.put()
                        self.redirect('/blog/%s' % post_id)
                    else:
                        error = "content can't be empty!"
                        self.render("editcomment.html", p=looked_up_post,
                                    comments=comments, content=content,
                                    error=error)
            else:
                self.render("notyours.html")
        else:
            self.redirect("/login")
