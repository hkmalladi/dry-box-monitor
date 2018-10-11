import socket
import fcntl
import struct
import Adafruit_DHT as dht
import httplib, urllib
import time
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO

lcd = CharLCD(numbering_mode=GPIO.BOARD,cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])
sleep = 15

key = 'EW2LDPHO42P399DK'

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s', ifname[:15])
    )[20:24])

while True:
    h,t = dht.read_retry(dht.DHT22, 4)
    lcd.cursor_pos = (0, 0)
    lcd.clear()
    lcd.write_string('T={0:0.1f}C, H={1:0.1f}%'.format(t, h))
    lcd.cursor_pos = (1, 0)
    try:
        lcd.write_string(get_ip_address('wlan0'))
    except:
        print('Failed to get IP address')
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
