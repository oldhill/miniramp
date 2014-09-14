import json
import logging
import operator

import webapp2

from utils import soundcloud_utils


class RecommendationHandler(webapp2.RequestHandler):
  """Recommends artists based on who the input artist follows.

  Gets the input artist's "followings" (all artists they follow) then gets the 
  followings' followings, then counts artist occurrences in the entire set and 
  returns the top followed artists as recommendations.
  """
  
  def get(self, artistUsername):
    """ Handle request, process data, return top 8 followed artists in json
    """
    artist_id = soundcloud_utils.username_to_user_id(artistUsername)
    followings = soundcloud_utils.get_followings(artist_id)

    # Handle case w here artist does not follow any artists
    if not followings: 
      return 

    # Log each followed artist, then log all of their followings as well
    artist_tracker = {}
    for artist in followings:
      artist_tracker = self._log_or_increment(artist, artist_tracker)
      next_followings = soundcloud_utils.get_followings(artist['id'])
      for artist in next_followings:
        artist_tracker = self._log_or_increment(artist, artist_tracker)

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
  def _log_or_increment(artist, artist_tracker):
    """ Keep track of how many users in our group of interest follow @artist
    """
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
