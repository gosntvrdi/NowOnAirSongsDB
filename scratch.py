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

#iterate through playlist.txt list and save each song to a database
i = 0
while i < len(latestPlaylistSongs):
    song = latestPlaylistSongs[i]
    query_string = urllib.parse.urlencode({"search_query": song})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    try:
        link = ('http://www.youtube.com/watch?v=' + search_results[0])
    except IndexError:
        link = ('https://www.youtube.com/watch?v=l6A4qnAX5Gw')
    videoPafy = pafy.new(link)
    best = videoPafy.getbestvideo()
    videompv = best.url
    #connect to database
    clientID = 'YammatFM'
    songDB = song
    youtubeLinkDB = videompv
    playlistName = os.path.basename(str(', '.join(playlists))) #convert list to string and remove brackets
    playlistName = os.path.basename(playlistName).replace('.txt', '')  # remove .txt from playlist name
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
    conn = mariadb.connect(host='192.168.150.251', user='videostream', database='songsDB')
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO playlists (songName, youtubeLink, clientID, date, playlistName) VALUES (%s, %s, %s, %s, %s)
                   ON DUPLICATE KEY UPDATE date = VALUES(date), playlistName = VALUES(playlistName)""", (songDB, youtubeLinkDB, clientID, timestamp, playlistName))
    conn.commit()
    i += 1




