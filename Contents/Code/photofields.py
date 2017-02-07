####################################################################################################
#	Helper file for ExportTools
# Written by dane22 on the Plex Forums, UKDTOM on GitHub
#
# This one contains the valid fields and attributes for photos
# 
# To disable a field not needed, simply put a # sign in front of the line, and it'll be ommited.
# After above, a PMS restart is sadly req. though
# Note though, that this will be overwritten, if/when this plugin is updated
#
# If level has the number 666 in it, a column named 'PMS Media Path' will
# automaticly be added to the end
####################################################################################################

# Fields that contains a timestamp and should return a date
dateTimeFields = ['addedAt', 'updatedAt', 'lastViewedAt']

# Fields that contains a timestamp and should return a time
timeFields =['duration']

# Levels that only req. a single call towards PMS
singleCall = ['Level 1', 'Level 2', 'Level 3']

# Define rows and element name for level 1 (Single call)
Level_1 = [
	('Media ID' , '@ratingKey'),
	('Title' , '@title'),
	('Summary' , '@summary'),
	('Originally Available At' , '@originallyAvailableAt'),
	('Added At' , '@addedAt'),
	('Updated At' , '@updatedAt')
	]	

Level_2 = [
	('Media Width', 'Media/@width'),
	('Media Height', 'Media/@height'),
	('Media Aspect Ratio', 'Media/@aspectRatio'),
	('Media Container', 'Media/@container'),
	('Media Title', 'Media/@title')
	]

Level_3 = [
	('Part File', 'Media/Part/@file'),
	('Part Size', 'Media/Part/@size'),
	('Part Size as Bytes', 'Media/Part/@size'),
	('Part Container', 'Media/Part/@container'),
	('Part Orientation', 'Media/Part/@orientation')
	]

Level_4 = [
	('Accessible' , 'Media/Part/@accessible'),	
	('Exists' , 'Media/Part/@exists')
	]

Level_5 = [
	]

Level_6 = [
	]

Level_7 = [
	]

Level_8 = [
	]

Level_9 = [
	]

Level_666 = [
	]

