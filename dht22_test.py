import Adafruit_DHT as dht
import httplib, urllib
import time

sleep = 15

key = 'Enter your ThingSpeak API key'

while True:
    h,t = dht.read_retry(dht.DHT22, 4)
    print ('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t, h))
    params = urllib.urlencode({'field1': h, 'field2':t, 'key':key })
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        conn.close()
    except:
        print "connection failed"
    time.sleep(sleep)
