# Miniramp extremely early, WIP version...

import os
import json
import urllib2

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

    # 'resolve' URL is necessary to get info based on artist's
    # username instead of user ID number.
    # Info: http://developers.soundcloud.com/docs/api/reference#resolve
    resolveUrl = 'http://api.soundcloud.com/resolve.json?url='
    knownUrl = 'http://soundcloud.com/' + artistUsername + '&client_id=YOUR_CLIENT_ID' 
    fullUrl = resolveUrl + knownUrl

    artistObject = urllib2.urlopen(fullUrl).read()

    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(artistObject)


app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/recommender/(\w+)', Recommender),
], debug=True)
