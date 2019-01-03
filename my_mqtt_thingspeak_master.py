#!/usr/bin/python3
from __future__ import print_function
import paho.mqtt.publish as publish
import psutil
import string
import random
import requests, os


# Everything ok? Zet debug to <False> instead of <True>
debug = True

# Modify URL if this is not running on localhost
host_port='http://localhost:8080'

# Replace idx=<xxxx> with your idx device number according your RaspPi setup (Setup-->Devices)
idx=<xxxx>

# The ThingSpeak Channel ID.
# Replace <YOUR-CHANNEL-ID> with your channel ID.
channelID = "<YOUR-CHANNEL-ID>"

# The Write API Key for the channel.
# Replace <YOUR-CHANNEL-WRITEAPIKEY> with your write API key.
writeAPIKey = "<YOUR-CHANNEL-WRITEAPIKEY>"

# The Hostname of the ThingSpeak MQTT broker.
mqttHost = "mqtt.thingspeak.com"

# You can use any Username.
mqttUsername = "whatever"

# Your <MQTT-API-KEY> from Account > My Profile.
mqttAPIKey ="<MQTT-API-KEY>"

# Set your clientID, replace <MY-CLIENTID> with your own text string if you like
clientID="<MY-CLIENTID>"

# Set the transport mode to WebSockets.
tTransport = "websockets"
tPort = 80


topic = "channels/" + channelID + "/publish/" + writeAPIKey
parameters={'type': 'devices', 'rid': idx }

resp = requests.get(host_port+'/json.htm', params=parameters)
results = resp.json()['result']
data = results[0]['Data']

# Modify if needed for your purpose! This is to cleanup data like "39.7 C" or "36.4%"
data=data.rstrip(' %C')

if debug:
    print("Request:  ", resp.request.url)
    print("Response: ", resp.text)
    print("Data:     ", data)

if (resp.status_code != 200) or (resp.json()['status'] != 'OK'):
    print('Error getting domotics json result {}'.format(resp.status_code))
    print('Result json data: ', results)
    exit(1)



# build the payload string.
#payload = "field1=" + str(data) + "&field2=" + str(data2)
payload = "field1=" + str(data)

# attempt to publish this data to the topic.
try:
	publish.single(topic, payload, hostname=mqttHost, transport=tTransport, port=tPort,auth={'username':mqttUsername,'password':mqttAPIKey})
	if debug: print ("Published Data Field 1 =", data ," to host: " , mqttHost , " clientID= " , clientID)
except (KeyboardInterrupt):
	exit(1)
except:
	if debug: print ("There was an error while publishing the data.")
	exit(1)

exit(0)
