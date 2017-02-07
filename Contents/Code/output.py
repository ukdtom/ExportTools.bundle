####################################################################################################
#	Helper file for ExportTools
# This one handles output
####################################################################################################

import xlsxwriter
import csv
import json
import misc
import os, io
import urllib2

import sys
import encodings

extension = ''
writer = ''
targetfile = ''


''' Create the output file, based on section title, timestamp and output type '''
def createFile(sectionKey, sectionType, title):
	global newtitle
	# Type of export
	global extension
	extension = '.' + Prefs['Output_Format']
	# Placeholder for return array
	retVal =[]
	if sectionType == 'playlists':
		myMediaURL = misc.GetLoopBack() + sectionKey
		playListType = title
		title = XML.ElementFromURL(myMediaURL, timeout=float(consts.PMSTIMEOUT)).get('title')
	else:
		myMediaURL = misc.GetLoopBack() + '/library/sections/' + sectionKey + "/all"
	Log.Debug("Path to medias in selection is %s" %(myMediaURL))
	# Get current date and time
	timestr = time.strftime("%Y%m%d-%H%M%S")
	# Generate Output FileName
	if sectionType == 'show':
		myLevel = Prefs['TV_Level']
	elif sectionType == 'movie':
		myLevel = Prefs['Movie_Level']
	elif sectionType == 'artist':
		myLevel = Prefs['Artist_Level']
	elif sectionType == 'photo':
		myLevel = Prefs['Photo_Level']
	elif sectionType == 'playlists':
		myLevel = Prefs['PlayList_Level']
	else:
		myLevel = ''
	# Remove invalid caracters, if on Windows......
	newtitle = re.sub('[\/[:#*?"<>|]', '_', title).strip()
	if sectionType == 'playlists':
		outFile = os.path.join(Prefs['Export_Path'], consts.NAME, 'Playlist-' + newtitle + '-' + myLevel + '-' + timestr + extension)
	else:
		if Prefs['Auto_Path']:
			# Need to grap the first location for the section
			locations = XML.ElementFromURL('http://127.0.0.1:32400/library/sections/', timeout=float(consts.PMSTIMEOUT)).xpath('.//Directory[@key="' + sectionKey + '"]')[0]
			location = locations[0].get('path')
			outFile = os.path.join(location, consts.NAME, newtitle + '-' + myLevel + '-' + timestr + extension)
			if not os.path.exists(os.path.join(location, consts.NAME)):
				os.makedirs(os.path.join(location, consts.NAME))
				Log.Debug('Auto Created directory named: %s' %(os.path.join(location, consts.NAME)))
			else:
				Log.Debug('Auto directory named: %s already exists' %(os.path.join(location, consts.NAME)))
		else:
			outFile = os.path.join(Prefs['Export_Path'], consts.NAME, newtitle + '-' + myLevel + '-' + timestr + extension)
	# Add what we got to the return array
	retVal.append(outFile)
	retVal.append(myMediaURL)
	# Posters ?
	global doPosters
	doPosters = False		
	if Prefs['Export_Posters']:	
		global posterDir
		if sectionType == 'show':
			if Prefs['TV_Level'] not in ["Level 1"]:
				doPosters = True
		if sectionType == 'movie':
			if Prefs['Movie_Level'] not in ["Level 1","Level 2","Special Level 1"]:
				doPosters = True
		if doPosters:
			posterDir = os.path.join(os.path.dirname(outFile), 'posters')
			if not os.path.exists(posterDir):
				os.makedirs(posterDir)
	return retVal

''' Create file header '''
def createHeader(outFile, sectionType, playListType = ''):
	global writer
	global targetfile
	global row
	global maxCol
	global fieldnames
	global columnwidth

	columnwidth = {}
	if sectionType == 'movies':
		fieldnames = movies.getMovieHeader(Prefs['Movie_Level'])
	elif sectionType == 'tvseries':
		fieldnames = tvseries.getTVHeader(Prefs['TV_Level'])
	elif sectionType == 'audio':
		fieldnames = audio.getMusicHeader(Prefs['Artist_Level'])
	elif sectionType == 'photo':
		fieldnames = photo.getHeader(Prefs['Photo_Level'])
	elif sectionType == 'playlist':
		fieldnames = playlists.getPlayListHeader(playListType, Prefs['PlayList_Level'])
	# Do we have an csv output here?
	if extension == '.csv':
		targetfile = io.open(outFile,'wb')
		# Create output file, and print the header
		writer = csv.DictWriter(targetfile, fieldnames=fieldnames, delimiter=Prefs['Delimiter'], quoting=csv.QUOTE_NONNUMERIC)
		writer.writeheader()
	elif extension == '.xlsx':
		targetfile = xlsxwriter.Workbook(outFile)
		writer = targetfile.add_worksheet(newtitle)
		writer.set_row(0, 20)  												# Set the height of Row 1 to 20.
		# Add bold formating
		bold = targetfile.add_format({'bold': True})
		row = 0
		col = 0
		for rowname in fieldnames:
			writer.write(row, col, rowname, bold)
			columnwidth[rowname] = len(rowname)
			col += 1
		row += 1
		maxCol = col
		if Prefs['Autosize_Row']:
			global wrap
			wrap = targetfile.add_format()
			wrap.set_text_wrap()
	return

''' Write row entry '''
def writerow(rowentry):
	global row
	global columnwidth
	if extension == '.csv':
		writer.writerow(rowentry)
	elif extension == '.xlsx':
		col = 0
		for key, value in rowentry.items():
			if Prefs['Autosize_Row']:
				writer.write(row, fieldnames.index(key), value, wrap)				
			else:
				writer.write(row, fieldnames.index(key), value)
			# Add lenght of field for later use with optimal column width, if needed
			if Prefs['Autosize_Column']:
				if columnwidth[key] < len(str(value)):
					columnwidth[key] = len(str(value))
			col += 1
		row += 1	
	if doPosters:
		posterUrl = 'http://127.0.0.1:32400/photo/:/transcode?width=' + str(Prefs['Poster_Width']) + '&height=' + str(Prefs['Poster_Hight']) + '&minSize=1&url=' + String.Quote(rowentry['Poster url'])
		try:
			thumbFile =  os.path.join(posterDir, rowentry['Media ID'] + '.jpg')
			thumb = HTTP.Request(posterUrl).content
			with io.open(thumbFile, 'wb') as handler:
				handler.write(thumb)
		except Exception, e:
			Log.Exception('Exception was %s' %(str(e)))

''' Close file again '''
def closefile():
	if extension == '.csv':
		targetfile.close
	elif extension == '.xlsx':
		# Add autofilter
		writer.autofilter(0, 0, row, maxCol-1)
		if Prefs['Autosize_Column']:
			setOptimalColWidth()
		# lock the header row
		writer.freeze_panes(1, 0)
		targetfile.close()

''' Keep track of column hight '''
def setOptimalColWidth():
	column = 1
	for width, value in columnwidth.items():
		idx = fieldnames.index(width)
		if Prefs['Line_Wrap']:
			if value > int(Prefs['Line_Length']):
				value = int(Prefs['Line_Length'])
		writer.set_column(idx, idx, int(value) + 1)
		column += 1
	return

