"""Miniramp extremely early version.

Recommends SoundCloud artists based on a user input artist. 
by oldhill.  MIT license.
"""
import json
import operator
import os
import urllib2

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
    artist_tracker = {}
    for artist in followings:
      artist_tracker = self._logOrIncrement(artist, artist_tracker)
      next_followings = utils.getFollowings(artist['id'])
      for artist in next_followings:
        artist_tracker = self._logOrIncrement(artist, artist_tracker)

    # Transform artists into a list, so we can sort and return the most-followed
    artist_list = []
    for name, artist_dict in artist_tracker.iteritems():
      artist_list.append(artist_dict)
    
    sorted_artists = sorted(artist_list, 
                            key = operator.itemgetter('occurrence_count'),
                            reverse = True)
    top_eight = sorted_artists[0:8]
    logging.info('Top 8 artists: %s of a total # of %s artists' % (top_eight, len(artist_list)))

    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(top_eight))

  @staticmethod
  def _logOrIncrement(artist, artist_tracker):
    if artist['username'] in artist_tracker:
      artist_tracker[artist['username']]['occurrence_count'] += 1
    else:
      artist_tracker[artist['username']] = {
        'username' : artist['username'],
        'id' : artist['id'],
        'occurrence_count' : 1,
        'url' : artist['permalink_url'],
      }
    return artist_tracker

    
app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/recommender/(\w+)', Recommender),
], debug=True)
