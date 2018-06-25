import datetime
import time
import mysql.connector as mariadb

ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
conn = mariadb.connect(host='192.168.150.251', user='videostream', database='songsDB')
cursor = conn.cursor()
cursor.execute("""INSERT INTO test (songName, youtubeLink, clientID, date) SELECT songName, youtubeLink, clientID, date FROM playlists
               ON DUPLICATE KEY UPDATE date = VALUES(date), youtubeLink = VALUES(youtubeLink)""")

conn.commit()