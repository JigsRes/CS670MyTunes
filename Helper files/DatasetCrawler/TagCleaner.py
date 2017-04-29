import pandas as pd
import collections
import os
from nltk.stem import PorterStemmer
import operator
import matplotlib.pyplot as plt
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
    base_directory = '/Users/sidverma/Desktop/'
    os.chdir(base_directory)
    #dirs = os.listdir(base_directory)
    globalTagsList = []
    for fn in ['Final0-1500.csv', 'Final1500-3000.csv']:
        df = pd.read_csv(fn)
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
            for t in set(iList):
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
        #print df.Tags.value_counts()
    return collections.Counter(globalTagsList)


def fooo(inTopTags):
    count = 0
    for fn in ['Final0-1500.csv', 'Final1500-3000.csv']:
        df = pd.read_csv(fn)
        # print df
        tagsCol = df['Tags']
        index = 0
        for i in tagsCol:
            if i == '[]':
                #df.set_value(index, 'Tags', emptyTag)
                index += 1
                continue
            if not isinstance(i, str):
                #df.set_value(index, 'Tags', emptyTag)
                index += 1
                continue
            i = i.replace('[', '')
            i = i.replace(']', '')
            i = i.replace('u\'', '')
            i = i.replace('\'', '')
            i = i.replace(' ', '#')
            i = i.replace(',#', ' ')
            if not len(i):
                #df.set_value(index, 'Tags', emptyTag)
                index += 1
                continue
            iList = i.split()
            isPresent = False
            for t in set(iList):
                t = t.lower()
                t = t.replace('#', ' ')
                tSubList = t.split()
                tSortedList = []
                for w in tSubList:
                    tSortedList.append(doStemming(w))
                tSortedList.sort()
                newTag = " ".join(tSortedList)
                print newTag
                #globalTagsList.append(newTag)
                if newTag in inTopTags:
                    isPresent = True
                    break
            print 'Processing..', index
            if isPresent:
                count+=1
            index += 1
        #df.to_csv('Final_Playlist_Users_0_1500_NEW.csv')
        #print df.Tags.value_counts()
    return count

freqDict = tagCleaner()
'''
for i in freqDict:
    print i, freqDict[i]
'''
print len(freqDict)
lists = sorted(freqDict.items(), key=operator.itemgetter(1), reverse = True)
i = 0
for tup in lists:
    i += 1
    if tup[1] < 5000:
        break
lists = lists[:i]
print 'Number of Unique Tags: ', i
print 'rows with tags :: ', str(fooo(lists))
#lists = sorted(freqDict.items()) # sorted by key, return a list of tuples

# f = open('frew', 'w')
# for tu in lists :
#     f.write(str(tu)+'\n')
# print 'done1'

xTicks, y = zip(*lists) # unpack a list of pairs into two tuples
#plt.figure(figsize = (90,30))
x = xrange(len(lists))
plt.xticks(x, xTicks, rotation=90)
# plt.plot(x,y)
plt.bar(x, y, color='b')
plt.show()
print 'done'