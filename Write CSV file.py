import csv
import pymysql
import time
import random
import urllib3
from urllib3 import PoolManager
import datetime
from datetime import datetime

#connect ke dbms berbasi api
connection = pymysql.connect(host='localhost',database='kumpulan',user='root',password='')
cursor=connection.cursor()

#memilih data dari dbms berbasis query
#query="SELECT datetime, sensorsatu, sensordua, sensortiga FROM totaldata;"
query="SELECT datetime, sensorsatu FROM totaldata;"
cursor.execute(query)
connection.commit()

#deklarasi variabel header field csv dan write api key dr thinkspeak
fields = ['datetime', 'field2', 'field3', 'field4', 'latitude', 'longitude', 'elevation', 'status']
write_api='ZK7J4CMO3WDQ7YTF'

#fetching yang dimasukkan dalam list untuk ditulis di file csv bersangkutan
list=[]
for row in cursor.fetchall():
    list.append(row)
    with open('data.csv', mode='w', newline='') as data:
        #wr = csv.DictWriter(data, fieldnames=fields)
        #wr.writeheader()
        wr = csv.writer(data, lineterminator = '\n', delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        wr.writerows(list)
print(list)
list=[]

cursor.close()
connection.close()
