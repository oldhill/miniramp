# custom SoundCloud REST API utility functions

import urllib2
import json

def userIdFromUsername(artistUsername):

   # 'resolve' URL is necessary to get info based on artist's
    # username instead of user ID number.
    # Info: http://developers.soundcloud.com/docs/api/reference#resolve
    resolveUrl = 'http://api.soundcloud.com/resolve.json?url='
    knownUrl = 'http://soundcloud.com/' + artistUsername + '&client_id=YOUR_CLIENT_ID' 
    fullUrl = resolveUrl + knownUrl
    
    artistString = urllib2.urlopen(fullUrl).read()
    artistObject = json.loads(artistString)

    return artistObject['id']
