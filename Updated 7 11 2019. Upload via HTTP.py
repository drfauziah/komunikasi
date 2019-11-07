import pymysql
import time
from time import sleep
import random
import urllib.request
import csv
import json

connection = pymysql.connect(host='localhost',database='client',user='root',password='')
cursor=connection.cursor()

query="SELECT field1 FROM tabeldata;"
cursor.execute(query)
connection.commit()

cursor.close()
connection.close()

#write_api='ZK7J4CMO3WDQ7YTF'
write_api='76fc160e-c8ce-447e-9a19-87098d3dba71'
read_api="eed5ef6e-9556-4d68-879e-edffc1f460e2"

url = "https://api.mwafa.net/channels/2/feeds.json?api_key=%s&results=1"%read_api
conn = urllib.request.urlopen(url).read().decode('UTF-8')
data = json.loads(conn)
list1 = data['feeds']

list = []
for key, value in list1[0].items():
    if key == "created_at":
        tanggal = list.append(value)

list1=[]
for row in cursor.fetchall():
    datasatu=row[0]
    #url = 'https://api.thingspeak.com/update?api_key=%s&field1=%s&field3=%s&field4=%s' %(write_api,datasatu,datadua,datatiga)
    url = 'https://api.mwafa.net/update.json?api_key=%s&field1=%s&start=%s'%(write_api, datasatu, tanggal)
    conn = urllib.request.urlopen(url)
    response = conn.read()
    print(datasatu)
    #time.sleep(1)

