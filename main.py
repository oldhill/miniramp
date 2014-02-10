# Miniramp extremely early, WIP version...

import os
import json

import webapp2
import jinja2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
  def get(self):
    # main page for user input
    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render())


class Recommender(webapp2.RequestHandler):
  def get(self, artistUsername):
    self.response.headers['Content-Type'] = 'application/json'
    artistObj = {
      'test' : artistUsername,
    }
    self.response.out.write(json.dumps(artistObj))


app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/recommender/(\w+)', Recommender),
], debug=True)
