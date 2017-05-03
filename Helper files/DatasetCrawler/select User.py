import pandas as pd
import os
import collections
import numpy as np
import operator
import matplotlib.pyplot as plt
import random

_PLAYLIST_SIZE_THRESHOLD = 200
_TAGS_THRESHOLD = 1
_GOOD_RATIO = 0.7
base_directory = 'C:/Users/007ri/OneDrive/Documents/GitHub/CS670MyTunes/Helper files/DatasetCrawler'
def getUserDataPlot():
    os.chdir(base_directory)
    df = pd.read_csv('Final.csv')
    groupFrame = df.groupby(by = 'Users')
    groupedUsers  = groupFrame.groups
    currrame = df.groupby(by='Users')
    X = xrange(len(groupedUsers))
    Y = []
    goodUsers = []
    for user in groupedUsers.keys():
        currFrame = groupFrame.get_group(user)
        songsPool = currFrame.Songs.tolist()
        Y.append(len(songsPool))
        if len(set(songsPool))>=_PLAYLIST_SIZE_THRESHOLD:
            goodUsers.append(user)
    freq = collections.Counter(Y)
    #for i in freq:
    #    print i, freq[i]
    '''
    #Uncomment to get teh plot
    choices = np.random.choice(len(X), 50)
    X_S = xrange(50)
    Y_S = []
    for c in choices:
        Y_S.append(Y[c])
    plt.bar(X_S, Y_S)
    plt.grid()
    plt.show()
    '''
    return goodUsers

def isGooodTagList(inTagsStr):
    inStrList = inTagsStr.split('#')
    intTagsList = [int(i) for i in inStrList]
    summation = sum(intTagsList)
    if summation<_TAGS_THRESHOLD:
        return False
    else:
        return True

def getGoodSongsPool():
    goodSongSet = set()
    os.chdir(base_directory)
    df = pd.read_csv('FinalTagroomMergedVecs.csv')
    songList = set()
    for i, row in df.iterrows():
        sng = row['Songs']
        if sng in songList:
            continue
        tagStr = row['Tags']
        if isGooodTagList(tagStr):
            songList.add(sng)
    return songList

def isUserGoodEnough(songsPool, goodSongsSet):
    goodSongsOfThisPool = 0
    for sng in songsPool:
        if sng in goodSongsSet:
            goodSongsOfThisPool+=1
    ratio = (1.0*goodSongsOfThisPool) / len(songsPool)
    if ratio >= _GOOD_RATIO:
        return True
    else:
        return False

def getTagetUsers():
    goodUsernames = getUserDataPlot()
    goodSongsSet = getGoodSongsPool()
    retTagetUsers = []
    os.chdir(base_directory)
    df = pd.read_csv('Final.csv')
    groupFrame = df.groupby(by='Users')
    for user in goodUsernames:
        currFrame = groupFrame.get_group(user)
        songsPool = set(currFrame.Songs.tolist())
        if isUserGoodEnough(songsPool, goodSongsSet):
            retTagetUsers.append(user)
    return retTagetUsers

tmp = getTagetUsers()
print len(tmp),'\nDone '


