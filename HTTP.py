import pymysql
import datetime
from datetime import datetime
import time
import urllib.request
#import requests
#import urllib3
#from urllib3 import PoolManager
import json
import urllib.parse

### Catatan :
### 1. Asumsi hanya 1 nilai sensor yang masuk per-row.

#API key
write_api='76fc160e-c8ce-447e-9a19-87098d3dba71'
read_api="eed5ef6e-9556-4d68-879e-edffc1f460e2"

#Memberi status system
status=1

try:
    while status == 1:
        #Mengetahui SATU DATA terakhir yang masuk ke server berdasarkan timestamp berbasis list
        #Sampling satu data cukup karena informasi yang dibutuhkan adalah ADA atau TIDAK
        #Bisa dilakukan sampling total, tapi tidak efektif dan berat di program

        url = "https://api.mwafa.net/channels/2/feeds.json?api_key=%s&results=1"%read_api
        conn = urllib.request.urlopen(url).read().decode('UTF-8')
        #data = conn.json()
        data = json.loads(conn)
        list_bantu = data['feeds']

        #Mencari ada atau tidak data yang masuk melalui nilai timestamp terakhir
        list_server = []
        if list_bantu == None:
                time_len_server=0
        else :
            for key, value in list_bantu[0].items():
                if key == "created_at":
                    list_server.append(value)
                    time_len_server=len(list_server) #1 atau 0 (ada atau tidak)

        #Algoritma apabila belum ada data yang masuk ke server
        if time_len_server == 0:
            
            #Membuka database client
            connection_client = pymysql.connect(host='localhost',database='client',user='root',password='')
            cursor=connection_client.cursor()

            #Memberi syntax SQL untuk mengumpulkan data timestamp dan nilai sensor - sensor dari tabel tabeldata
            query="select channel, created_at, field1, field2, field3, field4, field5, field6 from tabeldata;"
            cursor.execute(query)
            connection_client.commit()

            #Memberi nilai awal untuk entry_id, dimulai dari 1, karena belum ada data masuk
            entry_id=1

            #Mengambil data - data channel, timestamp, dan nilai sensor - sensor yang telah dikumpulkan berbasis fetchall
            for row in cursor.fetchall():
                channel=str(row[0]) #rownya menyesuaikan
                datetime=row[1] #rownya menyesuaikan
                coba = urllib.parse.quote(str(datetime))
                print(coba)
                datasatu=str(row[2]) #rownya menyesuaikan
                datadua=str(row[3]) #rownya menyesuaikan
                datatiga=str(row[4]) #rownya menyesuaikan
                dataempat=str(row[5]) #rownya menyesuaikan
                datalima=str(row[6]) #rownya menyesuaikan
                dataenam=str(row[7]) #rownya menyesuaikan
                
                print(channel, datetime, datasatu, datadua, datatiga, dataempat, datalima, dataenam) #opsional hehe
                
                ##Setelah data diambil, dipindahkan ke database bms (seperti client -> server)

                url = "https://api.mwafa.net/update.json?api_key=%s&channel=2&entry_id=%s&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s"%(write_api, entry_id, datasatu, datadua, datatiga, dataempat, datalima, dataenam)
                conn = urllib.request.urlopen(url)
                entry_id=entry_id+1
                print(conn)

            #Memberi delay (opsional)
            #Delay diberikan apabila ingin mengirimkan data tiap sekian sekon sekali
            #Delay dinonaktifkan apabila ingin mengirim data secara kontinu
            #time.sleep(5)

            #Menutup koneksi ke database client
            connection_client.close()

            #Memberi status
            status=1

        #Algoritma apabila ada data yang telah masuk
        if time_len_server != 0:
            url = "https://api.mwafa.net/channels/2/feeds.json?api_key=%s&results=1"%read_api
            conn = urllib.request.urlopen(url).read().decode('UTF-8')
            data = json.loads(conn)
            list1 = data['feeds']

            #Mencari ada atau tidak data yang masuk melalui nilai timestamp terakhir
            list_entry_id = []
            list_waktu_acuan = []
            for key, value in list1[0].items():
                if key == "entry_id":
                    list_entry_id.append(value)
                    entry_id = list_entry_id[0]+1
                if key == "created_at":
                    list_waktu_acuan.append(value)
                    waktu_server_acuan=list_waktu_acuan[0]
                    print(waktu_server_acuan)

            #Membuka database client
            connection_client = pymysql.connect(host='localhost',database='client',user='root',password='')
            cursor=connection_client.cursor()

            #Memberi syntax SQL untuk mengumpulkan data timestamp dan nilai sensor - sensor dari tabel client yang memiliki nilai timestamp lebih besar dari data terakhir yang masuk ke server
            query="select channel, created_at, field1, field2, field3, field4, field5, field6 from tabeldata where created_at>'%s';"%waktu_server_acuan.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(query)
            connection_client.commit()

            #Mengambil data - data timestamp dan nilai sensor - sensor yang telah dikumpulkan berbasis fetchall
            for row in cursor.fetchall():
                channel=str(row[0]) #rownya menyesuaikan
                datetime=row[1] #rownya menyesuaikan
                datasatu=str(row[2]) #rownya menyesuaikan
                datadua=str(row[3]) #rownya menyesuaikan
                datatiga=str(row[4]) #rownya menyesuaikan
                dataempat=str(row[5]) #rownya menyesuaikan
                datalima=str(row[6]) #rownya menyesuaikan
                dataenam=str(row[7]) #rownya menyesuaikan
                
                print(channel, datetime, datasatu, datadua, datatiga, dataempat, datalima, dataenam) #opsional hehe

                ##Setelah data diambil, dipindahkan ke database bms (seperti client -> server)

                url = 'https://api.mwafa.net/update.json?api_key=%s&channel=2&created_at=%s&entry_id=%s&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s'%(write_api, datetime, entry_id, datasatu, datadua, datatiga, dataempat, datalima, dataenam)
                conn = urllib.request.urlopen(url)
                entry_id=entry_id+1
               
            #Memberi delay
            #Delay diberikan apabila ingin mengirimkan data tiap sekian sekon sekali
            #Delay dinonaktifkan apabila ingin mengirim data secara kontinu
            #time.sleep(5)

            #Menutup koneksi ke database client
            connection_client.close()
            
            #Memberi status akhir
            status=1

#Perintah untuk mematikan program
except KeyboardInterrupt:
    status=0
