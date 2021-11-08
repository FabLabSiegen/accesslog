import paho.mqtt.client as mqtt
from print.views import *
def on_connect(client, userdata, rc, properties=None):
    client.subscribe("#")
    print("Connection returned result: " + mqtt.connack_string(rc))

def on_message(client, userdata, msg):
    # Do something
    # handle_msg(msg.topic, msg.payload)
    pass
    # print("%s %s" % (msg.topic, msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username="fablabmqtt",password="***REMOVED***")


client.connect("mqtt.fablab-siegen.de", 1883, 60)