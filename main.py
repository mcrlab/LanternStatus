
import requests
import unicornhathd as hat
import json
from paho.mqtt import client as mqtt

def from_hex(hex):
   data = {}
   r = int(hex[0:2], 16)
   g = int(hex[2:4], 16)
   b = int(hex[4:6], 16)
   return r,g,b

def set_pixel(i, hex):

   i = i * 3
   y = i % 15
   x = (i - y)/15
   x = (x * 3) + 1
   y = y + 1

   r,g,b = from_hex(hex)

   hat.set_pixel(x  , y,   r,g,b)
   hat.set_pixel(x+1, y,   r,g,b)
   hat.set_pixel(x  , y+1, r,g,b)
   hat.set_pixel(x+1, y+1, r,g,b)
   hat.show()

def on_connect(client, userdata, flags, rc):
   print("Connected")
   set_pixel(21, "00FF00")
   client.subscribe("ping");

def on_message(client, userdata, msg):
   data = json.loads(msg.payload)
   for light in lights:
      if light['address'] == data['id']:
         set_pixel(light['x'], data['color'])



try:
   hat.clear()

   r = requests.get("http://localhost/lights")
   lights = r.json()
   set_pixel(20, "00FF00")
   client = mqtt.Client("status") 
   client.username_pw_set(username="lantern",password="ilovelamp")
   client.on_connect = on_connect;
   client.on_message = on_message
   client.connect("localhost", 1883)
   client.loop_forever()

except KeyboardInterrupt:
  hat.off()
