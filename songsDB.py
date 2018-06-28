import mysql.connector as mariadb
import pafy
import urllib.request
import urllib.parse
import re
import time
import datetime
import pyinotify
import os

#song gets inserted to songsDB every time Jazler sends NowOnAir.txt to FTP/NowOnAir

dirname = os.path.dirname(__file__)
file = os.path.join(dirname, '//share/Storage/04-PUBLIC/05-NOW_PLAYING/NowOnAir.txt')


def songDB():
    NowOnAir = open(file, encoding='utf-8').readline()
    NowOnAir = NowOnAir[7:]
    query_string = urllib.parse.urlencode({"search_query": NowOnAir})
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
    songDB = NowOnAir
    youtubeLinkDB = videompv
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
    conn = mariadb.connect(host='192.168.150.251', user='videostream', database='songsDB')
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO songsDB (songName, youtubeLink, clientID, date) VALUES (%s, %s, %s, %s)
                   ON DUPLICATE KEY UPDATE date = VALUES(date)""", (songDB, youtubeLinkDB, clientID, timestamp))
    conn.commit()
    conn.close()


class ModHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, evt):
        songDB()


handler = ModHandler()
wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(file, pyinotify.IN_CLOSE_WRITE)
notifier.loop()

