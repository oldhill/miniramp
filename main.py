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
  """
  Main page where user inputs artist, gets recommendations back
  """
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render())


class Recommender(webapp2.RequestHandler):
  """
  Generates recommendations based on user input artist. 

  Gets the input artist's "followings" (all artists they follow)
  then gets the followings' followings and puts them all in a 
  structure, then finally counts the frequency and picks the 5 "most
  followed" artists to recommend.
  """
  def get(self, artistUsername):

    artistId = utils.userIdFromUsername(artistUsername)
    followings = utils.getFollowings(artistId)

    bigSet = {}

    for followedArtist in followings:
      # first level
      myName = followedArtist['username']
      myId = followedArtist['id']
      myUrl = followedArtist['permalink_url']

      bigSet[myName] = {
        'username' : myName,
        'id' : myId,
        'occurrenceCount' : 1,
        'url' : myUrl,
      }
      
      # second level
      secondFollowings = utils.getFollowings(myId)
      for secondFollowedArtist in secondFollowings:
        secondName = secondFollowedArtist['username']
        if secondName in bigSet:
          bigSet[secondName]['occurrenceCount'] += 1
        else:
          bigSet[secondName] = {
            'username' : secondName,
            'id' : secondFollowedArtist['id'],
            'occurrenceCount' : 1,
            'url' : secondFollowedArtist['permalink_url']
          }


     
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(bigSet))


app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/recommender/(\w+)', Recommender),
], debug=True)
