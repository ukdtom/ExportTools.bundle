############################################################################
# Helper file for ExportTools
# This one handles Photos
############################################################################

import misc
import photofields


def getHeader(PrefsLevel):
    '''
    This function will return the header for the CSV file for Photos
    '''
    fieldnames = ()
    if PrefsLevel.startswith('Special Level'):
        if PrefsLevel == 'Special Level 1':
            fieldnames = misc.getLevelFields(photofields.SLevel_1, fieldnames)
        if PrefsLevel == 'Special Level 2':
            fieldnames = misc.getLevelFields(photofields.SLevel_2, fieldnames)
        if PrefsLevel == 'Special Level 3':
            fieldnames = misc.getLevelFields(photofields.SLevel_3, fieldnames)
        if PrefsLevel == 'Special Level 4':
            fieldnames = misc.getLevelFields(photofields.SLevel_4, fieldnames)
        if PrefsLevel == 'Special Level 666':
            fieldnames = misc.getLevelFields(
                photofields.SLevel_666,
                fieldnames)
        if PrefsLevel == 'Special Level 666-2':
            fieldnames = misc.getLevelFields(
                photofields.SLevel_666,
                fieldnames)
        # Do we need the PMS path?
        if '666' in PrefsLevel:
            fieldnames.append('PMS Media Path')
        return fieldnames
    # Level 1 fields
    fieldnames = misc.getLevelFields(
        photofields.Level_1,
        fieldnames)
    # Basic fields
    if PrefsLevel in [
            'Level 2',
            'Level 3',
            'Level 4',
            'Level 5',
            'Level 6',
            'Level 7',
            'Level 8',
            'Level 666']:
        fieldnames = misc.getLevelFields(
            photofields.Level_2,
            fieldnames)
    # Extended fields
    if PrefsLevel in [
            'Level 3',
            'Level 4',
            'Level 5',
            'Level 6',
            'Level 7',
            'Level 8',
            'Level 666']:
        fieldnames = misc.getLevelFields(
            photofields.Level_3,
            fieldnames)
    # Extreme fields
    if PrefsLevel in [
            'Level 4',
            'Level 5',
            'Level 6',
            'Level 7',
            'Level 8',
            'Level 666']:
        fieldnames = misc.getLevelFields(
            photofields.Level_4,
            fieldnames)
    # Extreme 2 (Part) level
    if PrefsLevel in ['Level 5', 'Level 6', 'Level 7', 'Level 8', 'Level 666']:
        fieldnames = misc.getLevelFields(photofields.Level_5, fieldnames)
    # Extreme 3 level
    if PrefsLevel in ['Level 6', 'Level 7', 'Level 8', 'Level 666']:
        fieldnames = misc.getLevelFields(photofields.Level_6, fieldnames)
    # PMS Path also needs to be exported
    if '666' in PrefsLevel:
        fieldnames.append('PMS Media Path')
    return fieldnames


def getInfo(myMedia, myRow, level=None):
    '''
    This function will return the info for photo
    '''
    if level:
        prefsLevel = level
    else:
        prefsLevel = Prefs['Photo_Level']      
    if 'Special' in prefsLevel:
        if prefsLevel == 'Special Level 1':
            myRow = misc.getItemInfo(myMedia, myRow, photofields.SLevel_1)
        elif prefsLevel == 'Special Level 2':
            myRow = misc.getItemInfo(myMedia, myRow, photofields.SLevel_2)
        elif prefsLevel == 'Special Level 3':
            myRow = misc.getItemInfo(myMedia, myRow, photofields.SLevel_3)
        elif prefsLevel == 'Special Level 4':
            myRow = misc.getItemInfo(myMedia, myRow, photofields.SLevel_4)
        elif prefsLevel == 'Special Level 666':
            myRow = misc.getItemInfo(myMedia, myRow, photofields.SLevel_666)
        if '666' in prefsLevel:
            myRow = misc.getMediaPath(myMedia, myRow)
        return myRow
    else:
        # Get Simple Info
        myRow = misc.getItemInfo(myMedia, myRow, photofields.Level_1)
        # Get Basic Info
        if prefsLevel in [
                'Level 2',
                'Level 3',
                'Level 4',
                'Level 5',
                'Level 6',
                'Level 7',
                'Level 8',
                'Level 666']:
            myRow = misc.getItemInfo(
                myMedia,
                myRow,
                photofields.Level_2)
        # Get Extended Info
        if prefsLevel in [
                'Level 3',
                'Level 4',
                'Level 5',
                'Level 6',
                'Level 7',
                'Level 8',
                'Level 666']:
            myRow = misc.getItemInfo(myMedia, myRow, photofields.Level_3)
        # Get Extreme Info
        if prefsLevel in [
                'Level 4',
                'Level 5',
                'Level 6',
                'Level 7',
                'Level 8',
                'Level 666']:
            myRow = misc.getItemInfo(myMedia, myRow, photofields.Level_4)
        # Get Extreme 2 Info
        if prefsLevel in [
                'Level 5',
                'Level 6',
                'Level 7',
                'Level 8',
                'Level 666']:
            myRow = misc.getItemInfo(myMedia, myRow, photofields.Level_5)
        # Get Extreme 3 Info
        if prefsLevel in ['Level 6', 'Level 7', 'Level 8', 'Level 666']:
            myRow = misc.getItemInfo(myMedia, myRow, photofields.Level_6)
        # Get Media Path as well
        if '666' in prefsLevel:
            myRow = misc.getMediaPath(myMedia, myRow)
        return myRow
