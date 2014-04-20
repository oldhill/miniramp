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
    artist_id = utils.userIdFromUsername(artistUsername)
    followings = utils.getFollowings(artist_id)

    # Handle case w here artist does not follow any artists
    if not followings: 
      return 

    # Log each followed artist, then log all of their followings as well
    artistTracker = {}
    for artist in followings:
      artistTracker = self._logOrIncrement(artist, artistTracker)
      next_followings = utils.getFollowings(artist['id'])
      for artist in next_followings:
        artistTracker = logOrIncrement(artist, artistTracker)

    # Find and return the most followed artists
    sortedArtists = sorted(artistsList, 
                           key = operator.itemgetter('occurrenceCount'),
                           reverse = True)
    topEight = sortedArtists[0:8]

    #debug
    logging.info(topEight)
    logging.info('Total # of artists: ' + str(len(artistsList)))

    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(topEight))

  @staticmethod
  def _logOrIncrement(artist, artistTracker):
    if artist['username'] in artistTracker:
      artistTracker[artist['username']]['occurrenceCount'] += 1
    else:
      artistTracker[artist['username']] = {
        'username' : artist['username'],
        'id' : artist['id'],
        'occurrenceCount' : 1,
        'url' : artist['permalink_url'],
      }
    return artistTracker

    
app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/recommender/(\w+)', Recommender),
], debug=True)
