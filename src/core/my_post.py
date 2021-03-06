from src.handler import Handler
from src.model.post import Post


class MyPost(Handler):
    def get(self):
        if self.user:
            posts = Post.all().filter('owner_id = ', self.user.key()).order('-created')
            self.render('blog/front_blog.html', posts=posts, owner=True)
        else:
            self.redirect('/login')    
