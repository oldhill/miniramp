"""Recommends SoundCloud artists based on who an input artist follows
"""

import os
import urllib2

import jinja2
import webapp2

from utils import recommender


JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True
)


class MainHandler(webapp2.RequestHandler):
  """Main page where user inputs artist, gets recommendations back.
  """
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render())

   
app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/recommender/(\w+)', recommender.RecommendationHandler),
], debug=True)
