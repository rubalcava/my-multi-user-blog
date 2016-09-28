from BlogHandler import BlogHandler
from models import *
from globalstuff import myglobals
from google.appengine.ext import db

class NewComment(BlogHandler):
    def get(self, post_id):
        if self.user:
            # look up the post by id and get its stuff to populate form
            gql_lookup = Post.gql("WHERE post_id = :post_id", post_id=post_id)
            looked_up_post = gql_lookup.get()
            comments = Comment.all().order('-created')

            self.render('newcomment.html', p=looked_up_post,
                        comments=comments)
        else:
            self.redirect('/login')

    def post(self, post_id):
        if self.user:
            content = self.request.get('content')
            author_id = self.request.cookies.get('user_id').split('|')[0]
            author_name = User.by_id(long(author_id)).name

            if content:
                c = Comment(parent=myglobals.comment_key(), author_name=author_name,
                            author_id=author_id, post_id=post_id, content=content)

                c_key = c.put()
                c_returned = db.get(c_key)
                c_returned.comment_id = str(c_key.id())
                c_returned.comment_key = str(c_key)
                c_returned.put()
                # when postpage handler is invoked with redirect, comment wasn't
                # ready yet. had to add something to give it enough time so comment
                # would render properly.
                c_returned2 = db.get(c_key)

                self.redirect('/blog/%s' % str(post_id))
            else:
                error = "comment can't be empty!"
                gql_lookup = Post.gql("WHERE post_id = :post_id", post_id=post_id)
                looked_up_post = gql_lookup.get()

                self.render("newcomment.html", content=content, p=looked_up_post,
                            error=error)
        else:
            self.redirect("/login")
