####################################################################################################
#	Helper file for dane22
# This one handles misc functions
#
# Increment version for all new functions and fixes
#
####################################################################################################

VERSION = '0.0.0.5'

from textwrap import wrap, fill
import re
import datetime
import moviefields
import audiofields
import tvfields
import photofields
import dateutil.parser as parser

import sys
import os
import math
import consts


####################################################################################################
# This function will return the version of the misc module
####################################################################################################
def getVersion():
    return VERSION

####################################################################################################
# This function will return a valid token from plex.tv
####################################################################################################


def getToken():
    userName = Prefs['Plex_User']
    userPwd = Prefs['Plex_Pwd']
    myUrl = 'https://plex.tv/users/sign_in.json'
    # Create the authentication string
    base64string = String.Base64Encode('%s:%s' % (userName, userPwd))
    # Create the header
    MYAUTHHEADER = {}
    MYAUTHHEADER['X-Plex-Product'] = consts.DESCRIPTION
    MYAUTHHEADER['X-Plex-Client-Identifier'] = consts.APPGUID
    MYAUTHHEADER['X-Plex-Version'] = consts.VERSION
    MYAUTHHEADER['Authorization'] = 'Basic ' + base64string
    MYAUTHHEADER['X-Plex-Device-Name'] = consts.NAME
    # Send the request
    try:
        httpResponse = HTTP.Request(myUrl, headers=MYAUTHHEADER, method='POST')
        myToken = JSON.ObjectFromString(httpResponse.content)[
            'user']['authentication_token']
        Log.Debug('Response from plex.tv was : %s' %
                  (httpResponse.headers["status"]))
    except:
        Log.Critical(
            'Exception happend when trying to get a token from plex.tv')
        Log.Critical('Returned answer was %s' % httpResponse.content)
        Log.Critical('Status was: %s' % httpResponse.headers)
        return ''
    return myToken

####################################################################################################
# This function will return the loopback address
####################################################################################################


def GetLoopBack():

    # For now, simply return the IPV4 LB Addy, until PMS is better with this
    return 'http://127.0.0.1:32400'

    try:
        httpResponse = HTTP.Request(
            'http://[::1]:32400/web', immediate=True, timeout=5)
        return 'http://[::1]:32400'
    except:
        return 'http://127.0.0.1:32400'

####################################################################################################
# This function will return info from an array, defined in an xpath
####################################################################################################


def GetArrayAsString(Media, Field, default=''):
    Fields = Media.xpath(Field)
    if not Fields:
        Fields = ['']
    Field = ''
    for myField in Fields:
        if myField == None:
            myField = default
        if myField == '':
            myField = default
        if Field == '':
            Field = myField
        else:
            Field = Field + Prefs['Seperator'] + myField
    return WrapStr(fixCRLF(Field)).encode('utf8')

####################################################################################################
# This function will return info from extended page for movies
####################################################################################################


def GetExtInfo(ExtInfo, myField, default=''):
    try:
        myLookUp = WrapStr(ExtInfo.xpath('Media/@' + myField)[0])
        if not myLookUp:
            myLookUp = WrapStr(default)
    except:
        myLookUp = WrapStr(default)
#		Log.Debug('Failed to lookup field %s. Reverting to default' %(myField))
    return myLookUp.encode('utf8')

####################################################################################################
# This function will return info from different parts of a movie
####################################################################################################


def GetMoviePartInfo(ExtInfo, myField, default=''):
    try:
        myLookUp = WrapStr(ExtInfo.get(myField))
        if not myLookUp:
            myLookUp = WrapStr(default)
    except:
        myLookUp = WrapStr(default)
#		Log.Debug('Failed to lookup field %s. Reverting to default' %(myField))
    return myLookUp.encode('utf8')

####################################################################################################
#	Pull's a field from the xml
####################################################################################################


def GetRegInfo(myMedia, myField, default=''):
    try:
        if myField in ['rating']:
            myLookUp = "{0:.1f}".format(float(myMedia.get(myField)))
        else:
            myLookUp = WrapStr(fixCRLF(myMedia.get(myField)))
        if not myLookUp:
            myLookUp = WrapStr(default)
    except:
        myLookUp = WrapStr(default)
#		Log.Debug('Failed to lookup field %s. Reverting to default' %(myField))
    return myLookUp.encode('utf8')

####################################################################################################
#	Pull's a field from the xml
####################################################################################################


def GetRegInfo2(myMedia, myField, default=consts.DEFAULT, key='N/A'):
    returnVal = ''
    global retVal
    retVal = ''
    try:
        fieldsplit = myField.rsplit('@', 1)
        # Single attribute lookup
        if fieldsplit[0] == '':
            try:
                if len(fieldsplit) == 2:
                    returnVal = myMedia.get(fieldsplit[1])
                    if returnVal in [None, '']:
                        returnVal = default
                    elif fieldsplit[1] in moviefields.dateTimeFields:
                        returnVal = ConvertDateStamp(returnVal)
                        if returnVal == '01/01/1970':
                            returnVal = default
                    elif fieldsplit[1] in moviefields.timeFields:
                        returnVal = ConvertTimeStamp(returnVal)
                        if returnVal == '01/01/1970':
                            returnVal = default
                    # IMDB or TheMovieDB?
                    elif fieldsplit[1] == 'guid':
                        return metaDBLink(returnVal, mediatype=myMedia.xpath('@type')[0]).encode('utf8')
            except:
                Log.Critical('Exception on field: ' + myField)
                returnVal = default
                return WrapStr(fixCRLF(returnVal)).encode('utf8')
        else:
            # Attributes from xpath
            try:
                retVals = myMedia.xpath(fieldsplit[0][:-1])
            except:
                retVals = []
                retVals[0] = myField
                pass
            for retVal2 in retVals:
                try:
                    # Get attribute
                    retVal = default
                    retVal = String.Unquote(retVal2.get(fieldsplit[1]))
                    # Did it exists?
                    if retVal in [None, '']:
                        retVal = default
                    # Is it a dateStamp?
                    elif fieldsplit[1] in moviefields.dateTimeFields:
                        retVal = ConvertDateStamp(retVal)
                    # Got a timestamp?
                    elif fieldsplit[1] in moviefields.timeFields:
                        retVal = ConvertTimeStamp(retVal)
                    # size conversion?
                    elif key == 'Part Size':
                        retVal = ConvertSize(retVal)
                    if returnVal == '':
                        returnVal = retVal
                    else:
                        returnVal = returnVal + Prefs['Seperator'] + retVal
                except Exception, e:
                    if returnVal != '':
                        returnVal = returnVal + Prefs['Seperator'] + retVal
                        pass
                    else:
                        returnVal = default
                        pass
        return WrapStr(fixCRLF(returnVal)).encode('utf8')
    except:
        returnVal = default

####################################################################################################
#	Fix CR/LF
####################################################################################################


def fixCRLF(myString):
    myString = myString.decode('utf-8').replace('\r\n', ' ')
    myString = myString.decode('utf-8').replace('\n', ' ')
    myString = myString.decode('utf-8').replace('\r', ' ')
    return myString

####################################################################################################
#	Wraps a string if needed
####################################################################################################


def WrapStr(myStr, default='N/A'):
    LineWrap = int(Prefs['Line_Length'])
    if myStr == None:
        myStr = default
    if Prefs['Line_Wrap']:
        return fill(myStr, LineWrap)
    else:
        return myStr

####################################################################################################
# This function will return a string in hh:mm from a millisecond timestamp
####################################################################################################


def ConvertTimeStamp(timeStamp):
    seconds = str(int(timeStamp) / (1000) % 60)
    if len(seconds) < 2:
        seconds = '0' + seconds
    minutes = str((int(timeStamp) / (1000 * 60)) % 60)
    if len(minutes) < 2:
        minutes = '0' + minutes
    hours = str((int(timeStamp) / (1000 * 60 * 60)) % 24)
    return hours + ':' + minutes + ':' + seconds

####################################################################################################
# This function will return a date string in ISO 8601 format from a millisecond timestamp
####################################################################################################


def ConvertDateStamp(timeStamp):
    return Datetime.FromTimestamp(float(timeStamp)).date().isoformat()

####################################################################################################
# This function will return fieldnames for a level
####################################################################################################


def getLevelFields(levelFields, fieldnames):
    fieldnamesList = list(fieldnames)
    for item in levelFields:
        fieldnamesList.append(str(item[0]))
    return fieldnamesList

####################################################################################################
# This function fetch the actual info for the element
####################################################################################################


def getItemInfo(et, myRow, fieldList):
    try:
        for item in fieldList:
            try:
                key = str(item[0])
                value = str(item[1])
                # Special deal for Sort Title
                if key == 'Sort title':
                    if Prefs['Sort_title']:
                        if consts.DEFAULT == GetRegInfo2(et, value, consts.DEFAULT, key=key):
                            element = GetRegInfo2(
                                et, '@title', consts.DEFAULT, key='Title')
                        else:
                            element = GetRegInfo2(
                                et, value, consts.DEFAULT, key=key)
               # Special deal for Original Title
                elif key == 'Original Title':
                    if Prefs['Original_Title']:
                        print 'Ged'
                        if consts.DEFAULT == GetRegInfo2(et, value, consts.DEFAULT, key=key):
                            element = GetRegInfo2(
                                et, '@title', consts.DEFAULT, key='Title')
                        else:
                            element = GetRegInfo2(
                                et, value, consts.DEFAULT, key=key)

                # Special guid extract of the language code
                elif key == 'MetaData Language':
                    element = et.get('guid')
                    if '?lang=' in element:
                        element = element[element.index('?lang=') + 6:]
                    if element == '':
                        element = consts.DEFAULT
                else:
                    element = GetRegInfo2(et, value, consts.DEFAULT, key=key)
                # Empty fields are still present, but with a length of 0
                if element == '':
                    element = consts.DEFAULT
                if key in myRow:
                    myRow[key] = myRow[key] + Prefs['Seperator'] + element
                else:
                    myRow[key] = element
            except Exception, e:
                Log.Exception('Exception in getItemInfo: ' + str(e))
                myRow[key] = 'error'
                continue
        return myRow
    except Exception, e:
        Log.Exception('Exception in getItemInfo: ' + str(e))

####################################################################################################
# This function will return the media path info for movies
####################################################################################################


def getMediaPath(myMedia, myRow):
        # Get tree info for media
    myMediaTreeInfoURL = GetLoopBack() + '/library/metadata/' + \
        GetRegInfo(myMedia, 'ratingKey') + '/tree'
    TreeInfo = XML.ElementFromURL(myMediaTreeInfoURL).xpath('//MediaPart')
    for myPart in TreeInfo:
        MediaHash = GetRegInfo(myPart, 'hash')
        PMSMediaPath = os.path.join(Core.app_support_path, 'Media',
                                    'localhost', MediaHash[0], MediaHash[1:] + '.bundle', 'Contents')
        myRow['PMS Media Path'] = PMSMediaPath.encode('utf8')
    return myRow

####################################################################################################
# This function converts Byte to best readable string
####################################################################################################


def ConvertSize(SizeAsString):
    size = float(SizeAsString)
    if (size == 0):
        return '0B'
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024, i)
    s = round(size / p, 2)
    return '%s %s' % (s, size_name[i])

####################################################################################################
# Returns a MetaDb link from a Guid
####################################################################################################


def metaDBLink(guid, mediatype='episode', default='N/A'):
    if 'local://' in guid:
        sTmp = default
        return sTmp
    linkID = guid[guid.index('://') + 3:guid.index('?lang')]
    if 'com.plexapp.agents.imdb' in guid:
        sTmp = 'http://www.imdb.com/title/' + linkID
    elif 'com.plexapp.agents.themoviedb' in guid:
        if mediatype == 'movie':
            sTmp = 'https://www.themoviedb.org/movie/' + linkID
        elif mediatype == 'episode':
            sTmp = 'https://www.themoviedb.org/tv/' + linkID
    elif 'com.plexapp.agents.thetvdb' in guid:
        sTmp = 'https://thetvdb.com/?tab=series&id=' + linkID
    elif 'com.plexapp.agents.anidb' in guid:
        sTmp = 'https://anidb.net/perl-bin/animedb.pl?show=anime&aid=' + linkID
    elif 'com.plexapp.agents.data18' in guid:
        sTmp = 'http://www.data18.com/movies/' + linkID
    else:
        sTmp = default
    return sTmp
