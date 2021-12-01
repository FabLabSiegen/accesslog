import os

import paho.mqtt.client as mqtt
from print.views import handle_msg

def on_connect(client, userdata, rc, properties=None):
    try:
        client.subscribe(os.environ.get("MQTT_TOPIC"))
        print("Connection returned result: " + mqtt.connack_string(rc))
    except Exception as e:
        print(e)

def on_message(client, userdata, msg):
    handle_msg(msg.topic, msg.payload)

def on_disconnect(client, userdata, rc):
    client.loop_stop(force=False)
    if rc != 0:
        print("Unexpected disconnection.")
    else:
        print("Disconnected")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.username_pw_set(username=os.environ.get("MQTT_USER", "mqtt"),password=os.environ.get("MQTT_PASSWORD", "mqtt"))
try:
    client.connect(os.environ.get("MQTT_URL", "mqtt"), 1883, 60)
except Exception as e:
    print(e)
    print("hier")