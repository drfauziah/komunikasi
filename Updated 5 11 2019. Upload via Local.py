import pymysql
import datetime
from datetime import datetime
import time
import requests

### Catatan :
### 1. Asumsi hanya 1 nilai sensor yang masuk per-row.

#Memberi status system
write_api='76fc160e-c8ce-447e-9a19-87098d3dba71'
status=1

try:
    while status == 1:
        #Membuka database bms
        connection_bms = pymysql.connect(host='45.118.132.253',database='kumisteb_thingspeak',user='kumisteb_ts',password='dienteraja')
        cursor=connection_bms.cursor()

        #Mengetahui SATU DATA terakhir yang masuk ke server berdasarkan timestamp berbasis list
        #Sampling satu data cukup karena informasi yang dibutuhkan adalah ADA atau TIDAK
        #Bisa dilakukan sampling total, tapi tidak efektif dan berat di program
        query="select created_at from feeds limit 1;"
        cursor.execute(query)
        connection_bms.commit()
        list_server=[]
        for row in cursor.fetchall():
            list_server.append(row[0])
        time_len_server=len(list_server) #1 atau 0 (ada atau tidak)

        #Menutup koneksi database bms
        connection_bms.close()

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
                datasatu=str(row[2]) #rownya menyesuaikan
                datadua=str(row[3]) #rownya menyesuaikan
                datatiga=str(row[4]) #rownya menyesuaikan
                dataempat=str(row[5]) #rownya menyesuaikan
                datalima=str(row[6]) #rownya menyesuaikan
                dataenam=str(row[7]) #rownya menyesuaikan
                print(channel, datetime, datasatu, datadua, datatiga, dataempat, datalima, dataenam) #opsional hehe
                
                ##Setelah data diambil, dipindahkan ke database bms (seperti client -> server)

                url = 'https://api.mwafa.net/update.json?api_key=%s&channel=%s&created_at=%s&entry_id=%s&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s'%(write_api, channel, datetime, entry_id, datasatu, datadua, datatiga, dataempat, datalima, dataenam)
                conn = urllib.request.urlopen(url)
                entry_id=entry_id+1

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
            #Membuka database bms
            connection_bms = pymysql.connect(host='45.118.132.253',database='kumisteb_thingspeak',user='kumisteb_ts',password='dienteraja')
            cursor=connection_bms.cursor()

            #Mengetahui nilai timestamp satu data terakhir yang telah masuk
            query="select max(created_at) from feeds;"
            cursor.execute(query)
            connection_bms.commit()
            for row in cursor.fetchall():
                waktu_server_acuan=row[0]
            
            #Memberi syntax SQL untuk mengetahui nilai entry_id berdasarkan nilai timestamp data terakhir
            query="select entry_id from feeds where created_at = '%s';"%waktu_server_acuan
            cursor.execute(query)
            connection_bms.commit()

            #Mengetahui nilai entry_id yang masuk ke server berdasarkan timestamp terakhir yang masuk yang akan digunakan sebagai nilai entry_id awal
            list_entry=[]
            for row in cursor.fetchall():
                list_entry.append(row[0])
            entry_id=list_entry[0]+1

            #Menutup koneksi ke database bms
            connection_bms.close()

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

                #Membuka database bms
                connection_bms = pymysql.connect(host='45.118.132.253',database='kumisteb_thingspeak',user='kumisteb_ts',password='dienteraja')
                cursor=connection_bms.cursor()

                #Memberi syntax SQL untuk memasukkan data channel, timestamp, entry_id dan nilai sensor - sensor dari tabel totaldata
                query="insert into feeds (channel, created_at, entry_id, field1, field2, field3, field4, field5, field6) values ('2', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');"%(datetime, entry_id, datasatu, datadua, datatiga, dataempat, datalima, dataenam)
                cursor.execute(query)
                connection_bms.commit()
                entry_id=entry_id+1

                #Menutup koneksi ke database bms
                connection_bms.close()

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
