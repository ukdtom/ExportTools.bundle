#########################################################################
# Helper file for ExportTools
# This one handles playlists
#########################################################################

import misc
import consts


def getPlayListHeader(listtype, level):
    '''
    This function will return the header for the CSV file for playlists
    '''
    if listtype == 'video':
        # Video list Simple
        fieldnames = (
            'Playlist ItemID',
            'Media ID',
            'Type',
            'Studio',
            'TV-Show',
            'Title',
            'Rating',
            'Summary',
            'Year',
            'Duration',
            'File Name')
        # Video Basic fields
        if (
            level in [
                'Basic',
                'Extended',
                'Extreme',
                'Extreme 2',
                'Extreme 3']):
            fieldnames = fieldnames + (
                'Content Rating',
                'Tagline',
                'Originally Available At',
                'Added At',
                'Updated At')
    elif listtype == 'audio':
        # Audio list Simple
        fieldnames = (
            'Playlist ItemID',
            'Media ID',
            'Type',
            'Artist',
            'Album',
            'Title',
            'Original Title',
            'Summary',
            'Year',
            'Duration',
            'File Name')
        # Audio Basic fields
        if (
            level in [
                'Basic',
                'Extended',
                'Extreme',
                'Extreme 2',
                'Extreme 3']):
            fieldnames = fieldnames + (
                'Rating Count',
                'Added At',
                'Updated At')
    elif listtype == 'photo':
        # Photo list Simple
        fieldnames = (
            'Playlist ItemID',
            'Media ID',
            'Type',
            'Title',
            'Summary',
            'Year',
            'File Name')
        # Photo Basic fields
        if (
            level in [
                'Basic',
                'Extended',
                'Extreme',
                'Extreme 2',
                'Extreme 3']):
            fieldnames = fieldnames + (
                'Originally Available At',
                'Added At',
                'Updated At')
    return fieldnames


def getPlayListInfo(playListItem, myRow, playListType):
    '''
    This function will export and return the info for the Playlist
    '''
    # Get Simple Info
    if playListType == 'video':
        myRow = getPlayListSimpleVideo(playListItem, myRow)
        # Get Basic Info
        if Prefs['PlayList_Level'] in [
                'Basic',
                "Extended",
                "Extreme",
                "Extreme 2",
                "Extreme 3"]:
            myRow = getPlayListBasicVideo(playListItem, myRow)
    elif playListType == 'audio':
        myRow = getPlayListSimpleAudio(playListItem, myRow)
        if Prefs['PlayList_Level'] in [
                'Basic',
                "Extended",
                "Extreme",
                "Extreme 2",
                "Extreme 3"]:
            myRow = getPlayListBasicAudio(playListItem, myRow)
    elif playListType == 'photo':
        myRow = getPlayListSimplePhoto(playListItem, myRow)
        if Prefs['PlayList_Level'] in [
                'Basic',
                "Extended",
                "Extreme",
                "Extreme 2",
                "Extreme 3"]:
            myRow = getPlayListBasicPhoto(playListItem, myRow)
    return myRow


def getPlayListSimpleVideo(playListItem, myRow):
    '''
    This function will export and return the simple info for the
    Playlist for video types
    '''
    # Get the Playlist ItemID
    myRow['Playlist ItemID'] = misc.GetRegInfo(
        playListItem,
        'playlistItemID')
    # Get the media ID
    myRow['Media ID'] = misc.GetRegInfo(
        playListItem,
        'ratingKey')
    # Get media type
    myRow['Type'] = misc.GetRegInfo(
        playListItem,
        'type')
    # Get media title
    myRow['Title'] = misc.GetRegInfo(
        playListItem,
        'title')
    # Get TV-Show name
    myRow['TV-Show'] = misc.GetRegInfo(
        playListItem,
        'grandparentTitle',
        'N/A')
    # Get Rating
    myRow['Rating'] = misc.GetRegInfo(
        playListItem,
        'rating',
        'N/A')
    # Get Summary
    myRow['Summary'] = misc.GetRegInfo(
        playListItem,
        'summary',
        'N/A')
    # Get year
    myRow['Year'] = misc.GetRegInfo(
        playListItem,
        'year',
        'N/A')
    # Get studio
    myRow['Studio'] = misc.GetRegInfo(
        playListItem,
        'studio',
        'N/A')
    # Get Duration
    myRow['Duration'] = misc.ConvertTimeStamp(
        misc.GetRegInfo(
            playListItem,
            'duration',
            '0')).encode('utf8')
    # Grab the FileName(s)
    myRow['File Name'] = getFileNamesFromObject(playListItem)
    return myRow


def getPlayListSimpleAudio(playListItem, myRow):
    '''
    This function will export and return the simple info for the
    Playlist for audio types
    '''
    # Get the Playlist ItemID
    myRow['Playlist ItemID'] = misc.GetRegInfo(playListItem, 'playlistItemID')
    # Get the media ID
    myRow['Media ID'] = misc.GetRegInfo(playListItem, 'ratingKey')
    # Get media type
    myRow['Type'] = misc.GetRegInfo(playListItem, 'type')
    # Get media title
    myRow['Title'] = misc.GetRegInfo(playListItem, 'title')
    # Get Artist name
    myRow['Artist'] = misc.GetRegInfo(playListItem, 'grandparentTitle', 'N/A')
    # Get Album name
    myRow['Album'] = misc.GetRegInfo(playListItem, 'parentTitle', 'N/A')
    # Get Summary
    myRow['Summary'] = misc.GetRegInfo(playListItem, 'summary', 'N/A')
    # Get year
    myRow['Year'] = misc.GetRegInfo(playListItem, 'year', 'N/A')
    # Get Artist name
    myRow['Original Title'] = misc.GetRegInfo(
        playListItem,
        'originalTitle',
        'N/A')
    # Grab the FileName(s)
    myRow['File Name'] = getFileNamesFromObject(playListItem)
    # Get Duration
    myRow['Duration'] = misc.ConvertTimeStamp(misc.GetRegInfo(
        playListItem,
        'duration',
        '0')).encode('utf8')
    return myRow


def getPlayListSimplePhoto(playListItem, myRow):
    '''
    This function will export and return the simple info for
    the Playlist for photo types
    '''
    # Get the Playlist ItemID
    myRow['Playlist ItemID'] = misc.GetRegInfo(
        playListItem,
        'playlistItemID')
    # Get the media ID
    myRow['Media ID'] = misc.GetRegInfo(
        playListItem,
        'ratingKey')
    # Get media type
    myRow['Type'] = misc.GetRegInfo(
        playListItem,
        'type')
    # Get media title
    myRow['Title'] = misc.GetRegInfo(
        playListItem,
        'title')
    # Get Summary
    myRow['Summary'] = misc.GetRegInfo(
        playListItem,
        'summary',
        'N/A')
    # Get year
    myRow['Year'] = misc.GetRegInfo(
        playListItem,
        'year',
        'N/A')
    # Grab the FileName(s)
    myRow['File Name'] = getFileNamesFromObject(playListItem)
    return myRow


def getPlayListBasicVideo(playListItem, myRow):
    '''
    This function will export and return the basic info
    for the Playlist for movie/tv-shows types
    '''
    # Get Studio
    myRow['Studio'] = misc.GetRegInfo(playListItem, 'studio', 'N/A')
    # Get Content Rating
    myRow['Content Rating'] = misc.GetRegInfo(
        playListItem,
        'contentRating',
        'N/A')
    # Get Tagline
    myRow['Tagline'] = misc.GetRegInfo(playListItem, 'tagline', 'N/A')
    # Get Duration
    myRow['Duration'] = misc.ConvertTimeStamp(misc.GetRegInfo(
        playListItem,
        'duration',
        '0')).encode('utf8')
    # Get Originally Available At
    myRow['Originally Available At'] = misc.GetRegInfo(
        playListItem,
        'originallyAvailableAt',
        'N/A')
    # Get Added At
    myRow['Added At'] = misc.ConvertDateStamp(misc.GetRegInfo(
        playListItem,
        'addedAt',
        '0')).encode('utf8') + ' ' + misc.ConvertTimeStamp(
            misc.GetRegInfo(
                playListItem,
                'addedAt',
                '0')).encode('utf8')
    # Get Updated At
    myRow['Updated At'] = misc.ConvertDateStamp(
        misc.GetRegInfo(
            playListItem,
            'updatedAt',
            '0')).encode('utf8') + ' ' + misc.ConvertTimeStamp(
                misc.GetRegInfo(
                    playListItem,
                    'updatedAt',
                    '0')).encode('utf8')
    return myRow


def getPlayListBasicAudio(playListItem, myRow):
    '''
    This function will export and return the basic info for the
    Playlist for audio types
    '''
    # Get Rating count
    myRow['Rating Count'] = misc.GetRegInfo(playListItem, 'ratingCount', 'N/A')
    # Get Added At
    myRow['Added At'] = misc.ConvertDateStamp(misc.GetRegInfo(
        playListItem,
        'addedAt',
        '0')).encode('utf8') + ' ' + misc.ConvertTimeStamp(
            misc.GetRegInfo(
                playListItem,
                'addedAt',
                '0')).encode('utf8')
    # Get Updated At
    myRow['Updated At'] = misc.ConvertDateStamp(misc.GetRegInfo(
        playListItem,
        'updatedAt',
        '0')).encode('utf8') + ' ' + misc.ConvertTimeStamp(
            misc.GetRegInfo(
                playListItem,
                'updatedAt',
                '0')).encode('utf8')
    # Grab the FileName(s)
    myRow['File Name'] = getFileNamesFromObject(playListItem)
    return myRow


def getPlayListBasicPhoto(playListItem, myRow):
    '''
    This function will export and return the basic info for
    the Playlist for photo types
    '''
    # Get Originally Available At
    myRow['Originally Available At'] = misc.GetRegInfo(
        playListItem,
        'originallyAvailableAt',
        'N/A')
    # Get Added At
    myRow['Added At'] = misc.ConvertDateStamp(misc.GetRegInfo(
        playListItem,
        'addedAt',
        '0')).encode('utf8') + ' ' + misc.ConvertTimeStamp(
            misc.GetRegInfo(
                playListItem,
                'addedAt',
                '0')).encode('utf8')
    # Get Updated At
    myRow['Updated At'] = misc.ConvertDateStamp(misc.GetRegInfo(
        playListItem,
        'updatedAt',
        '0')).encode('utf8') + ' ' + misc.ConvertTimeStamp(
            misc.GetRegInfo(
                playListItem,
                'updatedAt',
                '0')).encode('utf8')
    return myRow


def getFileNamesFromObject(item):
    '''
    This function will return a string of filenames for an item
    '''
    # Grab the FileName(s)
    fileNames = []
    parts = item.xpath('.//Part')
    for part in parts:
        fileNames.append(part.get('file'))
    Field = ''
    for File in fileNames:
        if File is None:
            Field = consts.DEFAULT
        if File == '':
            Field = consts.DEFAULT
        if Field == '':
            Field = File
        else:
            Field = Field + Prefs['Seperator'] + File
    return Field
