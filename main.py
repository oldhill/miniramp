"""Miniramp extremely early version.

Recommends SoundCloud artists based on a user input artist. 
by oldhill.  MIT license.
"""

import json
import operator
import urllib2
import os

import jinja2
import logging
import webapp2

import utils.utils as utils # custom SoundCloud utils


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


class Recommender(webapp2.RequestHandler):
  """Recommends artists based on who the input artist follows.

  Gets the input artist's "followings" (all artists they follow) then gets the 
  followings' followings, then counts artist occurrences in the entire set and 
  returns the top followed artists as recommendations.
  """
  
  def get(self, artistUsername):
    artistId = utils.userIdFromUsername(artistUsername)
    followings = utils.getFollowings(artistId)
    if not followings: # artist does not follow any artists
      return 

    artistsObject = {}
    artistsList = []

    for followedArtist in followings:
      # first level
      myName = followedArtist['username']
      myId = followedArtist['id']
      myUrl = followedArtist['permalink_url']

      artistsObject[myName] = {
        'username' : myName,
        'id' : myId,
        'occurrenceCount' : 1,
        'url' : myUrl,
      }
      artistsList.append(artistsObject[myName])
      
      # second level
      secondFollowings = utils.getFollowings(myId)
      for secondFollowedArtist in secondFollowings:
        secondName = secondFollowedArtist['username']
        if secondName in artistsObject:
          artistsObject[secondName]['occurrenceCount'] += 1
        else:
          artistsObject[secondName] = {
            'username' : secondName,
            'id' : secondFollowedArtist['id'],
            'occurrenceCount' : 1,
            'url' : secondFollowedArtist['permalink_url']
          }
          artistsList.append(artistsObject[secondName])

    # Now that artistsObject is populated, sort and return the 
    # most followed artists
    sortedArtists = sorted(artistsList, 
                           key = operator.itemgetter('occurrenceCount'),
                           reverse = True)
    topEight = sortedArtists[0:8]

    #debug
    logging.info(topEight)
    logging.info('Total # of artists: ' + str(len(artistsList)))

    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(topEight))


app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/recommender/(\w+)', Recommender),
], debug=True)
