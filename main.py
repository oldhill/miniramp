""" Recommends SoundCloud artists based on who an input artist follows
"""

import os
import urllib2

import jinja2
import webapp2

from handlers import recommender

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True
)


class MainHandler(webapp2.RequestHandler):
  """ About page
  """
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('templates/index2.html')
    self.response.write(template.render())

class ScHandler(webapp2.RequestHandler):
  """ Main page where user inputs artist, gets recommendations back.
  """
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('templates/sc-index.html')
    self.response.write(template.render())


class CubesHandler(webapp2.RequestHandler):
  """ Render cubes
  """
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('templates/cubes.html')
    self.response.write(template.render())


class ProcHandler(webapp2.RequestHandler):
  """ Render processing sketch
  """
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('templates/processing.html')
    self.response.write(template.render())


app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/sc', ScHandler),
  ('/recommender/(\w+)', recommender.RecommendationHandler),
  ('/cubes', CubesHandler),
  ('/processing', ProcHandler),
], debug=True)
