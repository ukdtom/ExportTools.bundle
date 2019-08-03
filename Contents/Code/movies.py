###########################################################################
# Helper file for ExportTools
# This one handles movies
###########################################################################

import misc
import moviefields


def getMovieHeader(PrefsLevel):
    '''
    This function will return the header for the CSV file for movies
    '''
    fieldnames = ()
    if PrefsLevel.startswith('Special Level'):
        if PrefsLevel == 'Special Level 1':
            fieldnames = misc.getLevelFields(
                moviefields.SLevel_1,
                fieldnames)
        if PrefsLevel == 'Special Level 2':
            fieldnames = misc.getLevelFields(
                moviefields.SLevel_2,
                fieldnames)
        if PrefsLevel == 'Special Level 3':
            fieldnames = misc.getLevelFields(
                moviefields.SLevel_3,
                fieldnames)
        if PrefsLevel == 'Special Level 666':
            fieldnames = misc.getLevelFields(
                moviefields.SLevel_666,
                fieldnames)
        if PrefsLevel == 'Special Level 666-2':
            fieldnames = misc.getLevelFields(
                moviefields.SLevel_666,
                fieldnames)
        # Do we need the PMS path?
        if '666' in PrefsLevel:
            fieldnames.append('PMS Media Path')
        return fieldnames
    elif PrefsLevel == 'PlayCount 1':
        fieldnames = misc.getLevelFields(
                moviefields.PlayCount_1,
                fieldnames)
        return fieldnames
    # Level 1 fields
    fieldnames = misc.getLevelFields(
        moviefields.Level_1,
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
            moviefields.Level_2,
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
            moviefields.Level_3,
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
            moviefields.Level_4,
            fieldnames)
    # Extreme 2 (Part) level
    if PrefsLevel in ['Level 5', 'Level 6', 'Level 7', 'Level 8', 'Level 666']:
        fieldnames = misc.getLevelFields(moviefields.Level_5, fieldnames)
    # Extreme 3 level
    if PrefsLevel in ['Level 6', 'Level 7', 'Level 8', 'Level 666']:
        fieldnames = misc.getLevelFields(moviefields.Level_6, fieldnames)
    # PMS Path also needs to be exported
    if '666' in PrefsLevel:
        fieldnames.append('PMS Media Path')
    return fieldnames


def getMovieInfo(myMedia, myRow, prefsLevel):
    '''
    This function will return the info for movies
    '''
    if 'Special' in prefsLevel:
        if prefsLevel == 'Special Level 1':
            myRow = misc.getItemInfo(myMedia, myRow, moviefields.SLevel_1)
        elif prefsLevel == 'Special Level 2':
            myRow = misc.getItemInfo(myMedia, myRow, moviefields.SLevel_2)
        elif prefsLevel == 'Special Level 3':
            myRow = misc.getItemInfo(myMedia, myRow, moviefields.SLevel_3)
        elif prefsLevel == 'Special Level 4':
            myRow = misc.getItemInfo(myMedia, myRow, moviefields.SLevel_4)
        elif prefsLevel == 'Special Level 666':
            myRow = misc.getItemInfo(myMedia, myRow, moviefields.SLevel_666)
        if '666' in prefsLevel:
            myRow = misc.getMediaPath(myMedia, myRow)
        return myRow
    else:
        # Get Simple Info
        myRow = misc.getItemInfo(
            myMedia,
            myRow,
            moviefields.Level_1)
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
                moviefields.Level_2)
        # Get Extended Info
        if prefsLevel in [
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
                moviefields.Level_3)
        # Get Extreme Info
        if prefsLevel in [
                'Level 4',
                'Level 5',
                'Level 6',
                'Level 7',
                'Level 8',
                'Level 666']:
            myRow = misc.getItemInfo(
                myMedia,
                myRow,
                moviefields.Level_4)
        # Get Extreme 2 Info
        if prefsLevel in [
                'Level 5',
                'Level 6',
                'Level 7',
                'Level 8',
                'Level 666']:
            myRow = misc.getItemInfo(
                myMedia,
                myRow,
                moviefields.Level_5)
        # Get Extreme 3 Info
        if prefsLevel in [
                'Level 6',
                'Level 7',
                'Level 8',
                'Level 666']:
            myRow = misc.getItemInfo(
                myMedia,
                myRow,
                moviefields.Level_6)
        # Get Media Path as well
        if '666' in prefsLevel:
            myRow = misc.getMediaPath(
                myMedia,
                myRow)
        return myRow
