# Miniramp extremely early, WIP version...

import os

import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):

  def get(self):

    # homepage html and input


class Recommender(webapp2.RequestHandler):

  def get(self):

    # stuff
    

app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/recommender', Recommender),
], debug=True)
