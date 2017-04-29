import pandas as pd
import os
# metadata_base_dir = '/Users/sidverma/Documents/GitHub/CS670MyTunes/Helper files/DataSetCrawler_niksy/UserPlaylist1/'
# user_base_dir = 
#dirs = od.listdir('Home/QWERTY')
User_DF = pd.read_csv('/Users/sidverma/Documents/GitHub/CS670MyTunes/Datasets/Lastfm/Users_6000/users_playlist_new_0_1500.csv')
MetaData_DF = pd.read_csv('/Users/sidverma/Documents/GitHub/CS670MyTunes/Helper files/DataSetCrawler_niksy/UserPlaylist1/playlist0.csv')
User_DF = User_DF.truncate(after = 200, axis = 0)
MetaData_DF = MetaData_DF.truncate(after = 200, axis = 0)
print User_DF.shape, MetaData_DF.shape

User_DF['Match'] = User_DF.Songs == MetaData_DF.Songs
if False in set(User_DF['Match']):
	print "DataFrame Mismatch! Exiting Code!"
	exit()
print "All is Well!"
Combined_DF = pd.merge(User_DF, MetaData_DF, how='inner', on='Songs')
print User_DF.Match
#print Combined_DF
