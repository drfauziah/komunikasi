import random
import urllib3
from urllib3 import PoolManager
import time
from time import sleep

# Enter Your API key here
write_api='ZK7J4CMO3WDQ7YTF'

# Generating random data
x=0
while x <= 50:
	numb=random.randint(1,20)
	print(numb)
	# Sending the data to thingspeak
	module = urllib3.PoolManager()
	url = 'https://api.thingspeak.com/update?api_key=%s&field1=%s' %(write_api,numb)
	conn = module.request('GET',url)
	x=x+1
	time.sleep(20)

# Closing the connection
conn.close()
