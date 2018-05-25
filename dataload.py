import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys
def googlefecth(lat,lng,next_page_token):
    lat
    lng
    print(type(lat))
    api_key = 'your_api' #google api key
    datatype= 'your datatype' #such as restaurant
    if(next_page_token != '' ):
        serviceurl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+str(lat)+","+str(lng)+"&radius=1500&type="+datatype+"&key="+api_key+"&pagetoken="+next_page_token
    else:
         serviceurl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+lat+","+lng+"&radius=1500&type="+datatype+"&key="+api_key
    conn = sqlite3.connect('geodata.sqlite')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Locations (name TEXT,address TEXT,phone INTEGER,lat INTEGER,lng INTEGER,weekend TEXT,web TEXT,rating TEXT)''')
    url = serviceurl 
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    obj = json.loads(data)
    results = obj.get('results')
    number = 0
    for value in results:
        placeid = value.get('place_id')
        detailsurl = "https://maps.googleapis.com/maps/api/place/details/json?placeid="+placeid+"&key="+api_key
        ouh = urllib.request.urlopen(detailsurl)
        finaldata = ouh.read().decode()
        finalobj = json.loads(finaldata)
        v = finalobj.get('result')
        number = number + 1
        print(v.get('name'))
        name = v.get('name')
        web = v.get('website')
        rating = v.get('rating') 
        phone = v.get('formatted_phone_number')
        if(v.get('opening_hours')):
            weekdays = v.get('opening_hours').get('weekday_text')
            weekday = ','.join(map(str, weekdays))
        else:
            weekday = ''
        address = v.get('formatted_address')
        lat = v.get('geometry').get('location').get('lat')
        lng = v.get('geometry').get('location').get('lng')
        
        cur.execute('''INSERT INTO Locations (name,address,phone,lat,lng,weekend,web,rating)
                VALUES ( ?,?,?,?,?,?,?,? )''', (name,address,phone,lat,lng,weekday,web,rating,) )
        conn.commit()
        if number == 20:
          next_page_token = obj.get('next_page_token')

          googlefecth(lat,lng,next_page_token)
lat = input('Enter lat: ')
lng = input('Enter lng: ')
next_page_token =''
googlefecth(lat,lng,next_page_token)
