import json
import logging
import urllib2


def userIdFromUsername(artistUsername):
    # 'resolve' URL is necessary to get info based on artist's username instead of user ID number.
    # Docs: http://developers.soundcloud.com/docs/api/reference#resolve
    resolveUrl = 'http://api.soundcloud.com/resolve.json?url='
    knownUrl = 'http://soundcloud.com/' + artistUsername + '&client_id=YOUR_CLIENT_ID' 
    fullUrl = resolveUrl + knownUrl
    
    artistString = urllib2.urlopen(fullUrl).read()
    artistObject = json.loads(artistString)

    return artistObject['id']


def getFollowings(artistId):
    apiUrl = 'http://api.soundcloud.com/users/' + str(artistId);  
    followingsUrl = apiUrl + '/followings.json?client_id=YOUR_CLIENT_ID' 
    
    followingsString = urllib2.urlopen(followingsUrl).read()
    followingsObj = json.loads(followingsString)

    return followingsObj
