import pandas as pd
import collections
import os
from nltk.stem import PorterStemmer
stemCache = {}

def doStemming(w):
    if w in stemCache:
        return stemCache[w]
    stemmer = PorterStemmer()
    retVal = stemmer.stem(w)
    stemCache[w] = retVal
    return retVal

def tagCleaner():
    emptyTag = '$$NOTAG$$'
    base_directory = 'C:/Users/007ri/PycharmProjects/untitled/IR Proj'
    os.chdir(base_directory)
    #dirs = os.listdir(base_directory)
    globalTagsList = []
    df = pd.read_csv('Final_Playlist_Users_0_1500.csv')
    # print df
    tagsCol = df['Tags']
    index = 0
    for i in tagsCol:
        if i == '[]':
            df.set_value(index, 'Tags', emptyTag)
            index += 1
            continue
        if not isinstance(i, str):
            df.set_value(index, 'Tags', emptyTag)
            index += 1
            continue
        i = i.replace('[', '')
        i = i.replace(']', '')
        i = i.replace('u\'', '')
        i = i.replace('\'', '')
        i = i.replace(' ', '#')
        i = i.replace(',#', ' ')
        if not len(i):
            df.set_value(index, 'Tags', emptyTag)
            index += 1
            continue
        iList = i.split()
        for t in iList:
            t = t.lower()
            t = t.replace('#', ' ')
            tSubList = t.split()
            tSortedList = []
            for w in tSubList:
                tSortedList.append(doStemming(w))
            tSortedList.sort()
            newTag = " ".join(tSortedList)
            globalTagsList.append(newTag)
        index += 1
    #df.to_csv('Final_Playlist_Users_0_1500_NEW.csv')
    print df.Tags.value_counts()
    return collections.Counter(globalTagsList)

freqDict = tagCleaner()
'''
for i in freqDict:
    print i, freqDict[i]
'''
print len(freqDict)