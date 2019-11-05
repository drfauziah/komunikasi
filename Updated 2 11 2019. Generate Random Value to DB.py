import pymysql
import time
import random
import urllib3
import datetime
#from datetime import datetime

#connect ke dbms berbasis api
connection = pymysql.connect(host='localhost',database='client',user='root',password='')
cursor=connection.cursor()

entry_id=0
x=1
try:
    while x==1:
        #memberi timestamp (second)
        #now = datetime.now()
        #timestamp=datetime.timestamp(now)
        #convert timestamp (ms)
        #timestamp=1000*timestamp
        #print(timestamp)
        #memberi datetime real
        #timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").split(".")[0]
        #print (timestamp)
        #memberi nilai random ke file sensor satu, dua, tiga, dst
        channel=2
        s_satu=random.randint(35,40)
        s_dua=random.randint(1,20)
        s_tiga=random.randint(100,1000)
        #insert data ke dbms dengan query
        #query="INSERT INTO totaldata (datetime, sensorsatu, sensordua, sensortiga, latitude, longitude, elevation) VALUES (%s, %s, %s, %s, %s, %s, %s);"%(timestamp, s_satu, s_dua, s_tiga, lat, long, elevation)
        #query="INSERT INTO totaldata (datetime, sensorsatu) VALUES (%s, %s);"%(timestamp, s_satu)
        #query="INSERT INTO totaldata (sensorsatu) VALUES (%s);"%(s_satu)
        #query="INSERT INTO totaldata (sensordua) VALUES (%s);"%(s_dua)
        query="INSERT INTO tabeldata (channel, entry_id, field1) VALUES (%s, %s, %s);"%(channel, entry_id, s_satu)
        cursor.execute(query)
        connection.commit()
        print(s_satu, s_dua, s_tiga)
        entry_id=entry_id+1
        x=1
        time.sleep(1)

except KeyboardInterrupt:
    x=0
#disconnect dari dbms
connection.close

