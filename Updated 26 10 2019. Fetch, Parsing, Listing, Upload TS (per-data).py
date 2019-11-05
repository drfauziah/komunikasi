import pymysql
import time
import random
import urllib.request
import csv

connection = pymysql.connect(host='localhost',database='client',user='root',password='')
cursor=connection.cursor()

query="SELECT field1 FROM tabeldata;"
cursor.execute(query)
connection.commit()

cursor.close()
connection.close()

#write_api='ZK7J4CMO3WDQ7YTF'
write_api='76fc160e-c8ce-447e-9a19-87098d3dba71'

list1=[]
for row in cursor.fetchall():
    datasatu=row[0]
    #url = 'https://api.thingspeak.com/update?api_key=%s&field1=%s&field3=%s&field4=%s' %(write_api,datasatu,datadua,datatiga)
    url = 'https://api.mwafa.net/update.json?api_key=%s&field1=%s'%(write_api, datasatu)
    conn = urllib.request.urlopen(url)
    response = conn.read()
    print(datasatu)
    #time.sleep(1)
with open('test.csv', 'wb') as f:
    f.write(response)


