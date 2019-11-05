import pymysql
import time
import random
import urllib.request

#asumsi yang diambil dr database raspi A berisi DUA jenis sensor saja
#diinput ke feeds CHANNEL 2 FIELD 1 DAN FIELD 2
connection = pymysql.connect(host='localhost',database='kumpulan',user='root',password='')
cursor=connection.cursor()

query="SELECT sensorsatu, sensordua, sensortiga FROM totaldata;"
cursor.execute(query)
connection.commit()

cursor.close()
connection.close()

loop=1
entry_id=1
list1=[]
list2=[]
list3=[]

for row in cursor.fetchall():
    datasatu=row[0]
    datadua=row[1]
    datatiga=row[2]
    print(row[0], row[1], row[2])#opsional buat ngecek aja

    #koding untuk upload data ke dbase
    connection = pymysql.connect(host='localhost',database='bms',user='root',password='')
    cursor=connection.cursor()

    #koding sementara untuk parsing
    #asumsi tidak ada data 2 sensor (sensorsatu dan sensordua atau dengan sensortiga) masuk bersamaan
    if datasatu is not None:
        query="INSERT INTO feeds (channel, entry_id, field1) VALUES (2, %s, %s);"%(entry_id, datasatu)
        cursor.execute(query)
        connection.commit()

        list1.append(datasatu)

        entry_id=entry_id+1
    if datadua is not None:
        query="INSERT INTO feeds (channel, entry_id, field2) VALUES (2, %s, %s);"%(entry_id, datadua)
        cursor.execute(query)
        connection.commit()

        list2.append(datadua)

        entry_id=entry_id+1
    if datatiga is not None:
        query="INSERT INTO feeds (channel, entry_id, field3) VALUES (2, %s, %s);"%(entry_id, datatiga)
        cursor.execute(query)
        connection.commit()

        list3.append(datatiga)

        entry_id=entry_id+1
    if datasatu and datadua and datatiga is None:
        query="INSERT INTO feeds (channel, entry_id, field1, field2, field3) VALUES (2, %s, %s, %s, %s);"%(entry_id, Null, Null, Null)
        cursor.execute(query)
        connection.commit()
    
        list3.append(datatiga)
    
        entry_id=entry_id+1
    else :
        pass

    cursor.close()
    connection.close()   
print(list1)
print(list2)
print(list3)
