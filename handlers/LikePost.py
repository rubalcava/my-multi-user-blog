from BlogHandler import BlogHandler
from models import *
from globalstuff import myglobals

class LikePost(BlogHandler):
    def get(self, post_id):
        if self.user:
            # look up post to verify if current user is author
            gql_lookup = Post.gql("WHERE post_id = :post_id", post_id=post_id)
            looked_up_post = gql_lookup.get()
            current_user_id = str(self.user.key().id())
            author_user_id = str(looked_up_post.user_id)

            already_liked = False

            comments = Comment.all().order('-created')

            # get list of current user's liked posts and check
            # if user has already liked this one
            liked_posts = self.user.liked_posts
            if post_id in liked_posts:
                already_liked = True

            if already_liked is False:
                if current_user_id != author_user_id:
                    current_likes = looked_up_post.likes
                    looked_up_post.likes = current_likes + 1
                    looked_up_post.put()
                    self.user.liked_posts.append(post_id)
                    self.user.put()
                    self.render("permalink.html", post=looked_up_post,
                                comments=comments)
                else:
                    error = "you can't like your own posts"
                    self.render("permalink.html", post=looked_up_post,
                                error=error, comments=comments)
            else:
                error = "you already liked this post"
                self.render("permalink.html", post=looked_up_post,
                            error=error, comments=comments)
        else:
            self.redirect("/login")
