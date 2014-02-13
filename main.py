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

    bigSet = {}

    for followedArtist in followings:
      # first level
      myName = followedArtist['username']
      myId = followedArtist['id']

      bigSet[myName] = {
        'username' : myName,
        'id' : myId,
        'occurrenceCount' : 0,
      }
      
      # second level
      secondFollowings = utils.getFollowings(myId)
      for secondFollowedArtist in secondFollowings:
        myName = followedArtist['username']

        # increment count, or create new record
        if bigSet[myName]:
          bigSet[myName]['occurrenceCount'] += 1
        else:
          bigSet[myName] = {
            'username' : myName,
            'id' : followedArtist['id'],
            'occurrenceCount' : 0,
          }


     
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(bigSet))


app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/recommender/(\w+)', Recommender),
], debug=True)
