import mysql.connector as mariadb
import pafy
import urllib.request
import urllib.parse
import re
import time
import datetime
import os
import glob

#set working dir
dirname = os.path.dirname(__file__)
file = os.path.join(dirname, 'playlists/*.txt')

#get latest playlist.txt in dir
playlists = glob.glob(file)
latestPlaylist = max(playlists, key = os.path.getctime)
latestPlaylist = open(latestPlaylist, encoding='utf-8')

#get rid of 1st line in playlist.txt (header) and strip the /n (new line)
latestPlaylistSongs = latestPlaylist.readlines()[1:]
latestPlaylistSongs = [s.rstrip() for s in latestPlaylistSongs]
latestPlaylistSongs = ([s.replace('Direct File - ', '') for s in latestPlaylistSongs])





