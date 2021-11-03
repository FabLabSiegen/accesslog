import paho.mqtt.client as mqtt

def on_connect(client, userdata, rc):
    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    # Do something
    print(client + userdata + msg)
    pass

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)