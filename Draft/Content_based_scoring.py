#packages and libraries
import pandas as pd
import math
import time
import random
import sys
import os
import collections
import operator
split_ratio = 0.8
user_list = []
neighbours_list = []
scores_list = [] 

base_directory = '/Users/sidverma/Desktop/IR/'
os.chdir(base_directory)

DataSetFile = "Final.csv"   #Need to check the name of the file
DataSetSongFile = "FinalTagroomMergedVecs.csv"    # Need to check the name of this file
DataSetTagDictFile = "/Users/sidverma/Documents/GitHub/CS670MyTunes/Helper files/DatasetCrawler/FinalTagFreq.csv"


# reading the main File
frame = pd.read_csv(DataSetFile)
frame.drop(["Playtime", "Album", "Match" , "Listeners", "Playcount", "Duration", "Tags"], axis=1, inplace="True")

# reading the tags related file:
## Songs Based Scoring
frameSong = pd.read_csv(DataSetSongFile)
groupedSongs = frameSong.groupby(by="Songs")
groupsSongs = groupedSongs.groups
full_len = frameSong.shape[0]
### Users based grouping 
groupedUsers = frame.groupby(by="Users")
groupsUsers=groupedUsers.groups


# Using the dict for storing the IDF vector
df_dict = pd.read_csv(DataSetTagDictFile)
IDF_DICT = [math.log10((full_len/df_dict['Frequency'][i])) for i in xrange(df_dict.shape[0])]

def findmagnitude(input):
    return math.sqrt(sum(input[i]*input[i] for i in range(len(input))))

def normalizefunction(input):
    listmagnitude =  findmagnitude(input)
    if  listmagnitude == 0:
        return  input
    return [ float(input[i])/listmagnitude  for i in range(len(input)) ]

def cosinefunction(input1, input2):
    return sum(input1[i]*input2[i] for i in range(len(input1)))

def TF_IDF_generator(input):
    return_list = []
    for i in range(len(input)):
        if input[i]==0:
            val = IDF_DICT[i]
        else:
            val = (math.log10(input[i])+1)* IDF_DICT[i]
        return_list.append(val)
    return return_list



# calculating the user content based on the history
def Calculate_content_based_score(username):
    historyList = []
    user_group = groupedUsers.get_group(username)
    #print user_group.Songs
    Full_list = user_group.Songs.tolist()
    Train_list = Full_list[0:int(math.ceil(split_ratio*len(Full_list)))]
    #print Train_list
    for tracks in Train_list:
        print "Printing the length of the tags"
        tags_len = len(groupedSongs.get_group(tracks).Tags)
        tags_list = groupedSongs.get_group(tracks).Tags.tolist()
        historyListString =  str(tags_list[0]).split("$")
        historytempvec = []
        for itr in historyListString:
            historytempvec.append(int(itr))
        historyList.append (historytempvec)
    TF_listvec = [sum(x) for x in zip(*historyList)]
    print TF_listvec
    print len(TF_listvec)
    TF_IDF_listvec = TF_IDF_generator(TF_listvec)
    UserList_normalized = normalizefunction(TF_IDF_listvec)
    ScoringDict = collections.defaultdict(list)
    for allusers in groupsUsers.keys()[:10]:
        print allusers
        if allusers == username:
            continue
        for tracks in groupedUsers.get_group(allusers).Songs.tolist():
             if tracks in ScoringDict:
                 continue
             songtempvec = []
             #tags_len = len(groupedSongs.get_group(tracks).Tags)
             tags_list = groupedSongs.get_group(tracks).Tags.tolist()
             songlistString =  str(tags_list[0]).split("$")
             for itr in songlistString:
                  songtempvec.append(int(itr))
             TF_IDF_songvec = TF_IDF_generator(songtempvec)
             song_normalized = normalizefunction(TF_IDF_songvec)
             ScoringDict[tracks]= cosinefunction(UserList_normalized, song_normalized)
    print "I have reached here"

    reversesorteditems = sorted(ScoringDict.items(), key=operator.itemgetter(1), reverse=True)
    count = 0
    similar_neighbors=[]
    similarity_scores=[]
    for  items in reversesorteditems:
        if count == 300:
           break
        similar_neighbors.append(str(items[0]))
        similarity_scores.append(str(items[1]))                       
        count = count + 1      
    return similar_neighbors, similarity_scores

def calculate_for_all():
    for allusers in groupsUsers.keys()[:10]:
        print allusers
        user_list.append(allusers)
        [neb_list,score_list] =  Calculate_content_based_score(allusers)                    
        neighbours_list.append(neb_list)
        scores_list.append(score_list)

calculate_for_all()

df = pd.DataFrame(
    data={"Users": user_list, "Neigbours": neighbours_list, "Similarities": scores_list },
    columns=["Users", "Neighbours", "Similarities"])
df.to_csv("ContentBasedSimilarity.csv", sep=',')

    
