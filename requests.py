import urllib.request
import json
  
# api-endpoint
read_key = "eed5ef6e-9556-4d68-879e-edffc1f460e2"
write_key = "76fc160e-c8ce-447e-9a19-87098d3dba71"

url = "https://api.mwafa.net/update.json?api_key=%s$field1=40"%(write_key)

# sending get request and saving the response as response object 
r = urllib.request.urlopen(url)
  
# extracting data in json format 
#data = r.json()
print(r)

# extracting latitude, longitude and formatted address  
# of the first matching location 
#latitude = data['results'][0]['geometry']['location']['lat'] 
#longitude = data['results'][0]['geometry']['location']['lng'] 
#formatted_address = data['results'][0]['formatted_address'] 
  
# printing the output 
#print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
#      %(latitude, longitude,formatted_address))
