import json
import pymysql
import time
import random
import urllib3
from urllib3 import PoolManager

#connect ke dbms berbasi api
connection = pymysql.connect(host='localhost',database='kumpulan',user='root',password='')
cursor=connection.cursor()

#memilih data dari dbms berbasis query
query="SELECT datetime, sensorsatu, sensordua, sensortiga FROM totaldata;"
cursor.execute(query)
connection.commit()

#deklarasi variabel header field csv dan write api key dr thinkspeak
fields = ['datetime', 'field2', 'field3', 'field4', 'latitude', 'longitude', 'elevation', 'status']
write_api='ZK7J4CMO3WDQ7YTF'

#fetching yang dimasukkan dalam list untuk ditulis di file json bersangkutan
data={}
data['people'] = []
for row in cursor.fetchall():
    data['people'].append({
        'datetime': '%s'%row[0]
    })
with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)

cursor.close()
connection.close()
