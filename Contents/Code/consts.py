########################################################################
# Helper file for ExportTools
# This one handles global constants
########################################################################

# APP specific stuff
VERSION = ' V2.0.0.2'
NAME = 'ExportTools'
DESCRIPTION = 'Export Plex libraries to csv-files or xlsx-files'
ART = 'art-default.jpg'
ICON = 'icon-default.png'
PREFIX = '/applications/ExportTools'
APPGUID = '7608cf36-742b-11e4-8b39-00af17210b2'
PLAYLIST = 'playlist.png'
DEFAULT = 'N/A'

# How many items we ask for each time, when accessing a section
CONTAINERSIZEMOVIES = 30
CONTAINERSIZETV = 20
CONTAINERSIZEEPISODES = 30
CONTAINERSIZEAUDIO = 10
CONTAINERSIZEPHOTO = 20

# For slow PMS HW, we might need to wait some time here
PMSTIMEOUT = Prefs['TimeOut']
