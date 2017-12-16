####################################################################################################
#	Helper file for ExportTools
# This one handles TV-Shows
####################################################################################################

import misc
import tvfields
import consts
from lxml import etree as ET

STACKEDLABELS = ['cd', 'disc', 'disk', 'dvd', 'part', 'pt']

####################################################################################################
# This function will return the header for the CSV file for TV-Shows
####################################################################################################


def getTVHeader(PrefsLevel):
    fieldnames = ()
    # Show only stuff
    if PrefsLevel.startswith('Show Only'):
        fieldnames = misc.getLevelFields(tvfields.Show_1, fieldnames)
        if PrefsLevel in ['Show Only 2', 'Show Only 3']:
            fieldnames = misc.getLevelFields(tvfields.Show_2, fieldnames)
        if PrefsLevel in ['Show Only 3']:
            fieldnames = misc.getLevelFields(tvfields.Show_3, fieldnames)
        return fieldnames
    # Special stuff
    if PrefsLevel.startswith('Special Level'):
        if PrefsLevel == 'Special Level 1':
            fieldnames = misc.getLevelFields(tvfields.SLevel_1, fieldnames)
        if PrefsLevel == 'Special Level 2':
            fieldnames = misc.getLevelFields(tvfields.SLevel_2, fieldnames)
        if PrefsLevel == 'Special Level 3':
            fieldnames = misc.getLevelFields(tvfields.SLevel_3, fieldnames)
        if PrefsLevel == 'Special Level 4':
            fieldnames = misc.getLevelFields(tvfields.SLevel_4, fieldnames)
        if PrefsLevel == 'Special Level 666':
            fieldnames = misc.getLevelFields(tvfields.SLevel_666, fieldnames)
        if PrefsLevel == 'Special Level 666-2':
            fieldnames = misc.getLevelFields(tvfields.SLevel_666, fieldnames)
        # Do we need the PMS path?
        if '666' in PrefsLevel:
            fieldnames.append('PMS Media Path')
        return fieldnames
    # Level 1 fields
    fieldnames = misc.getLevelFields(tvfields.Level_1, fieldnames)
    # Basic fields
    if PrefsLevel in ['Level 2', 'Level 3', 'Level 4', 'Level 5', 'Level 6', 'Level 7', 'Level 8', 'Level 666']:
        fieldnames = misc.getLevelFields(tvfields.Level_2, fieldnames)
    # Extended fields
    if PrefsLevel in ['Level 3', 'Level 4', 'Level 5', 'Level 6', 'Level 7', 'Level 8', 'Level 666']:
        fieldnames = misc.getLevelFields(tvfields.Level_3, fieldnames)
    # Extreme fields
    if PrefsLevel in ['Level 4', 'Level 5', 'Level 6', 'Level 7', 'Level 8', 'Level 666']:
        fieldnames = misc.getLevelFields(tvfields.Level_4, fieldnames)
    # Extreme 2 (Part) level
    if PrefsLevel in ['Level 5', 'Level 6', 'Level 7', 'Level 8', 'Level 666']:
        fieldnames = misc.getLevelFields(tvfields.Level_5, fieldnames)
    # Extreme 3 level
    if PrefsLevel in ['Level 6', 'Level 7', 'Level 8', 'Level 666']:
        fieldnames = misc.getLevelFields(tvfields.Level_6, fieldnames)
    # Level 7
    if PrefsLevel in ['Level 7', 'Level 8', 'Level 666']:
        fieldnames = misc.getLevelFields(tvfields.Level_7, fieldnames)
    # PMS Path also needs to be exported
    if '666' in PrefsLevel:
        fieldnames.append('PMS Media Path')
    return fieldnames


####################################################################################################
# This function will return the info for tv-shows
####################################################################################################
def getTvInfo(myMedia, myRow):
    prefsLevel = Prefs['TV_Level']
    if prefsLevel in ['Show Only 1', 'Show Only 2']:
        myRow = misc.getItemInfo(myMedia, myRow, tvfields.Show_1)
        if prefsLevel == 'Show Only 2':
            myRow = misc.getItemInfo(myMedia, myRow, tvfields.Show_2)
        return myRow
    elif 'Special' in prefsLevel:
        if prefsLevel == 'Special Level 1':
            myRow = misc.getItemInfo(myMedia, myRow, tvfields.SLevel_1)
        elif prefsLevel == 'Special Level 2':
            myRow = misc.getItemInfo(myMedia, myRow, tvfields.SLevel_2)
        elif prefsLevel == 'Special Level 3':
            myRow = misc.getItemInfo(myMedia, myRow, tvfields.SLevel_3)
        elif prefsLevel == 'Special Level 4':
            myRow = misc.getItemInfo(myMedia, myRow, tvfields.SLevel_4)
        elif prefsLevel == 'Special Level 666':
            myRow = misc.getItemInfo(myMedia, myRow, tvfields.SLevel_666)
        if '666' in prefsLevel:
            myRow = misc.getMediaPath(myMedia, myRow)
        return myRow
    else:
        # Get Simple Info
        myRow = misc.getItemInfo(myMedia, myRow, tvfields.Level_1)
        # Get Basic Info
        if prefsLevel in ['Level 2', 'Level 3', 'Level 4', 'Level 5', 'Level 6', 'Level 7', 'Level 8', 'Level 666']:
            myRow = misc.getItemInfo(myMedia, myRow, tvfields.Level_2)
        # Get Extended Info
        if prefsLevel in ['Level 3', 'Level 4', 'Level 5', 'Level 6', 'Level 7', 'Level 8', 'Level 666']:
            myRow = misc.getItemInfo(myMedia, myRow, tvfields.Level_3)
        # Get Extreme Info
        if prefsLevel in ['Level 4', 'Level 5', 'Level 6', 'Level 7', 'Level 8', 'Level 666']:
            myRow = misc.getItemInfo(myMedia, myRow, tvfields.Level_4)
        # Get Extreme 2 Info
        if prefsLevel in ['Level 5', 'Level 6', 'Level 7', 'Level 8', 'Level 666']:
            myRow = misc.getItemInfo(myMedia, myRow, tvfields.Level_5)
        # Get Extreme 3 Info
        if prefsLevel in ['Level 6', 'Level 7', 'Level 8', 'Level 666']:
            myRow = misc.getItemInfo(myMedia, myRow, tvfields.Level_6)
        # Get Extreme 3 Info
        if prefsLevel in ['Level 7', 'Level 8', 'Level 666']:
            myRow = misc.getItemInfo(myMedia, myRow, tvfields.Level_7)
        # Get Media Path as well
        if '666' in prefsLevel:
            myRow = misc.getMediaPath(myMedia, myRow)
        return myRow


''' Export TV Show info only '''


def getShowOnly(myMedia, myRow, level):
    prefsLevel = Prefs['TV_Level']
    if prefsLevel in ['Show Only 1', 'Show Only 2', 'Show Only 3']:
        for key, value in tvfields.Show_1:
            element = myMedia.get(value[1:])
            if element == None:
                element = 'N/A'
            element = misc.WrapStr(misc.fixCRLF(element).encode('utf8'))
            if key == 'MetaDB Link':
                myRow[key] = misc.metaDBLink(element)
            elif key in myRow:
                myRow[key] = myRow[key] + Prefs['Seperator'] + element
            else:
                myRow[key] = element
    if prefsLevel in ['Show Only 2', 'Show Only 3']:
        for key, value in tvfields.Show_2:
            myRow[key] = misc.GetArrayAsString(
                myMedia, value, default=consts.DEFAULT)
    # Additional call needed for level 3
    if prefsLevel in ['Show Only 3']:
        directURL = misc.GetLoopBack() + '/library/metadata/' + \
            myRow['Media ID']
        directMedia = XML.ElementFromURL(
            directURL, timeout=float(consts.PMSTIMEOUT))
        for key, value in tvfields.Show_3:
            if key == 'MetaDB Link':
                myRow[key] = misc.metaDBLink(
                    str(directMedia.xpath('//Directory/@guid')))
            elif key == 'Collection':
                serieInfo = directMedia.xpath('//Directory/Collection')
                myCol = ''
                for collection in serieInfo:
                    if myCol == '':
                        myCol = collection.get('tag')
                    else:
                        myCol = myCol + \
                            Prefs['Seperator'] + collection.get('tag')
                    if myCol == '':
                        myCol = 'N/A'
                myRow[key] = myCol
            else:
                myRow[key] = misc.GetArrayAsString(
                    directMedia, value, default=consts.DEFAULT)
    return myRow
