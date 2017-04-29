### Code Block to Check Incomplete Playlists
import os
_BASE_DIRECTORY_ = []
idx = 0
for k in [0, 1, 3, 4, 5]:
	_BASE_DIRECTORY_.append('/Users/sidverma/Documents/GitHub/CS670MyTunes/Helper files/DataSetCrawler_niksy/UserPlaylist' + str(k+1) + '/')
	dirs = os.listdir(_BASE_DIRECTORY_[idx])
	idx += 1
	print dirs