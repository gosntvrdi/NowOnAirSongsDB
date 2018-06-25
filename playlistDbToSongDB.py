import datetime
import time
import mysql.connector as mariadb


#songDB gets updated with human verified youtubeLink every time user makes a change to his/her's playlist in database
ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
conn = mariadb.connect(host='192.168.150.251', user='videostream', database='songsDB')
cursor = conn.cursor()
cursor.execute("""INSERT INTO test (songName, youtubeLink, clientID, date) SELECT songName, youtubeLink, clientID, date FROM playlists
               ON DUPLICATE KEY UPDATE date = VALUES(date), youtubeLink = VALUES(youtubeLink), verifiedLink = 1""")

conn.commit()