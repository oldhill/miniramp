import json
import logging
import urllib2


def userIdFromUsername(artistUsername):
    artistUrl = 'http://soundcloud.com/%s&client_id=YOUR_CLIENT_ID' % artistUsername 
    
    # This 'resolve' prefix URL is necessary to get info by username rather than ID number.
    # doc: http://developers.soundcloud.com/docs/api/reference#resolve
    resolvePrefix = 'http://api.soundcloud.com/resolve.json?url='
    
    artistString = urllib2.urlopen(resolvePrefix + artistUrl).read()
    artistObject = json.loads(artistString)

    return artistObject['id']


def getFollowings(artistId):
    apiUrl = 'http://api.soundcloud.com/users/%s' % artistId 
    followingsUrl = apiUrl + '/followings.json?client_id=YOUR_CLIENT_ID' 
    
    followingsString = urllib2.urlopen(followingsUrl).read()
    followingsObj = json.loads(followingsString)

    return followingsObj
