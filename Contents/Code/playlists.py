####################################################################################################
#	Helper file for ExportTools
# This one handles playlists
####################################################################################################

import misc

####################################################################################################
# This function will return the header for the CSV file for playlists
####################################################################################################
def getPlayListHeader(listtype, level):
	if listtype == 'video':
		# Video list Simple
		fieldnames = ('Playlist ItemID',
				'Media ID',
				'Type', 
				'TV-Show',
				'Title',				
				'Rating',
				'Summary',
				'Year'
				)
		# Basic fields
		if (level in ['Basic','Extended','Extreme', 'Extreme 2', 'Extreme 3']):
			fieldnames = fieldnames + (
			'Studio',
			'Content Rating',
			'Tagline',
			'Duration',
			'Originally Available At',
			'Added At',
			'Updated At'
			)
	elif listtype == 'audio':
		# Audio list Simple
		fieldnames = ('Playlist ItemID',
				'Media ID',
				'Type', 
				'Artist',
				'Album',
				'Title',				
				'Summary',
				'Year'
				)
		# Basic fields
		if (level in ['Basic','Extended','Extreme', 'Extreme 2', 'Extreme 3']):
			fieldnames = fieldnames + (
				'Rating Count',
				'Duration',
				'Added At',
				'Updated At'
				)
	elif listtype == 'photo':
		# Photo list Simple
		fieldnames = ('Playlist ItemID',
				'Media ID',
				'Type', 
				'Title',				
				'Summary',
				'Year'
				)
		# Basic fields
		if (level in ['Basic','Extended','Extreme', 'Extreme 2', 'Extreme 3']):
			fieldnames = fieldnames + (
				'Originally Available At',
				'Added At',
				'Updated At'
			)
	return fieldnames

####################################################################################################
# This function will export and return the info for the Playlist
####################################################################################################
def getPlayListInfo(playListItem, myRow, playListType):
	# Get Simple Info
	if playListType == 'video':
		myRow = getPlayListSimpleVideo(playListItem, myRow)
		# Get Basic Info
		if Prefs['PlayList_Level'] in ['Basic', "Extended", "Extreme", "Extreme 2", "Extreme 3"]:
			myRow = getPlayListBasicVideo(playListItem, myRow)
	elif playListType == 'audio':
		myRow = getPlayListSimpleAudio(playListItem, myRow)
		if Prefs['PlayList_Level'] in ['Basic', "Extended", "Extreme", "Extreme 2", "Extreme 3"]:
			myRow = getPlayListBasicAudio(playListItem, myRow)
	elif playListType == 'photo':
		myRow = getPlayListSimplePhoto(playListItem, myRow)
		if Prefs['PlayList_Level'] in ['Basic', "Extended", "Extreme", "Extreme 2", "Extreme 3"]:
			myRow = getPlayListBasicPhoto(playListItem, myRow)
	return myRow

####################################################################################################
# This function will export and return the simple info for the Playlist for video types
####################################################################################################
def getPlayListSimpleVideo(playListItem, myRow):
	# Get the Playlist ItemID
	myRow['Playlist ItemID'] = misc.GetRegInfo(playListItem, 'playlistItemID')
	# Get the media ID
	myRow['Media ID'] = misc.GetRegInfo(playListItem, 'ratingKey')	
	# Get media type
	myRow['Type'] = misc.GetRegInfo(playListItem, 'type')	
	# Get media title
	myRow['Title'] = misc.GetRegInfo(playListItem, 'title')
	# Get TV-Show name
	myRow['TV-Show'] = misc.GetRegInfo(playListItem, 'grandparentTitle', 'N/A')
	# Get Rating
	myRow['Rating'] = misc.GetRegInfo(playListItem, 'rating', 'N/A')
	# Get Summary
	myRow['Summary'] = misc.GetRegInfo(playListItem, 'summary', 'N/A')
	# Get year
	myRow['Year'] = misc.GetRegInfo(playListItem, 'year', 'N/A')
	return myRow

####################################################################################################
# This function will export and return the simple info for the Playlist for audio types
####################################################################################################
def getPlayListSimpleAudio(playListItem, myRow):
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
	return myRow

####################################################################################################
# This function will export and return the simple info for the Playlist for audio types
####################################################################################################
def getPlayListSimplePhoto(playListItem, myRow):
	# Get the Playlist ItemID
	myRow['Playlist ItemID'] = misc.GetRegInfo(playListItem, 'playlistItemID')
	# Get the media ID
	myRow['Media ID'] = misc.GetRegInfo(playListItem, 'ratingKey')	
	# Get media type
	myRow['Type'] = misc.GetRegInfo(playListItem, 'type')	
	# Get media title
	myRow['Title'] = misc.GetRegInfo(playListItem, 'title')
	# Get Summary
	myRow['Summary'] = misc.GetRegInfo(playListItem, 'summary', 'N/A')
	# Get year
	myRow['Year'] = misc.GetRegInfo(playListItem, 'year', 'N/A')
	return myRow

####################################################################################################
# This function will export and return the basic info for the Playlist for movie/tv-shows types
####################################################################################################
def getPlayListBasicVideo(playListItem, myRow):
	# Get Studio
	myRow['Studio'] = misc.GetRegInfo(playListItem, 'studio', 'N/A')
	# Get Content Rating
	myRow['Content Rating'] = misc.GetRegInfo(playListItem, 'contentRating', 'N/A')
	# Get Tagline
	myRow['Tagline'] = misc.GetRegInfo(playListItem, 'tagline', 'N/A')
	# Get Duration
	myRow['Duration'] = misc.ConvertTimeStamp(misc.GetRegInfo(playListItem, 'duration', '0')).encode('utf8')
	# Get Originally Available At
	myRow['Originally Available At'] = misc.GetRegInfo(playListItem, 'originallyAvailableAt', 'N/A')
	# Get Added At
	myRow['Added At'] = misc.ConvertDateStamp(misc.GetRegInfo(playListItem, 'addedAt', '0')).encode('utf8') + ' ' + misc.ConvertTimeStamp(misc.GetRegInfo(playListItem, 'addedAt', '0')).encode('utf8')
	# Get Updated At
	myRow['Updated At'] = misc.ConvertDateStamp(misc.GetRegInfo(playListItem, 'updatedAt', '0')).encode('utf8') + ' ' + misc.ConvertTimeStamp(misc.GetRegInfo(playListItem, 'updatedAt', '0')).encode('utf8')
	return myRow

####################################################################################################
# This function will export and return the basic info for the Playlist for audio types
####################################################################################################
def getPlayListBasicAudio(playListItem, myRow):
	# Get Rating count
	myRow['Rating Count'] = misc.GetRegInfo(playListItem, 'ratingCount', 'N/A')
	# Get Duration
	myRow['Duration'] = misc.ConvertTimeStamp(misc.GetRegInfo(playListItem, 'duration', '0')).encode('utf8')
	# Get Added At
	myRow['Added At'] = misc.ConvertDateStamp(misc.GetRegInfo(playListItem, 'addedAt', '0')).encode('utf8') + ' ' + misc.ConvertTimeStamp(misc.GetRegInfo(playListItem, 'addedAt', '0')).encode('utf8')
	# Get Updated At
	myRow['Updated At'] = misc.ConvertDateStamp(misc.GetRegInfo(playListItem, 'updatedAt', '0')).encode('utf8') + ' ' + misc.ConvertTimeStamp(misc.GetRegInfo(playListItem, 'updatedAt', '0')).encode('utf8')
	return myRow

####################################################################################################
# This function will export and return the basic info for the Playlist for photo types
####################################################################################################
def getPlayListBasicPhoto(playListItem, myRow):
	# Get Originally Available At
	myRow['Originally Available At'] = misc.GetRegInfo(playListItem, 'originallyAvailableAt', 'N/A')
	# Get Added At
	myRow['Added At'] = misc.ConvertDateStamp(misc.GetRegInfo(playListItem, 'addedAt', '0')).encode('utf8') + ' ' + misc.ConvertTimeStamp(misc.GetRegInfo(playListItem, 'addedAt', '0')).encode('utf8')
	# Get Updated At
	myRow['Updated At'] = misc.ConvertDateStamp(misc.GetRegInfo(playListItem, 'updatedAt', '0')).encode('utf8') + ' ' + misc.ConvertTimeStamp(misc.GetRegInfo(playListItem, 'updatedAt', '0')).encode('utf8')
	return myRow

