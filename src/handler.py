import os
import jinja2
import webapp2
from model.security import make_secure_value
from model.security import check_secure_value

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    @staticmethod
    def render_str(template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_cookie(self, name, val):
        cookie_value = make_secure_value(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s|%s; Path=/' % (name, cookie_value))

    def read_cookie(self, name):
        cookie_val = self.request.cookies.get(name)

        if cookie_val:
            if check_secure_value(cookie_val):
                return True

        return False

    def login(self, user):
        self.set_cookie('user_id', str(user.key().id()))

    def logout(self):
        pass
