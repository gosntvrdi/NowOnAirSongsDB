import mysql.connector as mariadb
import pafy
import urllib.request
import urllib.parse
import re
import time
import datetime
import os
import glob


dirname = os.path.dirname(__file__)
file = os.path.join(dirname, 'playlists/*.txt')
playlists = glob.glob(file)
latestPlaylist = max(playlists, key = os.path.getctime)



print (latestPlaylist)



