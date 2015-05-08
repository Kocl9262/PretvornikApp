#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        self.render_template("hello.html")


class PretvorbaHandler(BaseHandler):
    def post(self):
        pretvorba1 = self.request.get("vnos1")
        pretvorba2 = self.request.get("vnos2")
        pretvorba1 = pretvorba1.replace(",", ".")
        pretvorba2 = pretvorba2.replace(",", ".")

        if pretvorba1 != "":
            rez1 = float(pretvorba1) * 0.62
            rez1 = pretvorba1 + "km = " + str(rez1) + "milj"
            rez1 = rez1.replace(".", ",")
        else:
            rez1 = ""

        if pretvorba2 != "":
            rez2 = float(pretvorba2) * 1.61
            rez2 = pretvorba2 + "milj = " + str(rez2) + "km"
            rez2 = rez2.replace(".", ",")
        else:
            rez2 = ""

        params = {"pretvorba1": pretvorba1, "pretvorba2": pretvorba2, "rez1": rez1, "rez2": rez2}
        self.render_template("pretvorba.html", params)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/pretvorba', PretvorbaHandler)
], debug=True)
