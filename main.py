# Miniramp extremely early, WIP version...

import os
import json
import urllib2

import webapp2
import jinja2

# custom SoundCloud utils
import utils

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

    artistId = utils.userIdFromUsername(artistUsername)
    followings = utils.getFollowings(artistId)
     
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(followings)


app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/recommender/(\w+)', Recommender),
], debug=True)
