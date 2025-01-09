#Implementing a MQTT broker using the Paho library 
import paho.mqtt.client as mqtt
import hashlib
#import time
import base64
#import json
import sqlite3


broker_address = "localhost"
broker_port = 1883

client = mqtt.Client()

client.connect(broker_address, broker_port, 60)

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe("sensor")

def on_message(client, userdata, msg):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    file_transfer_started = False
    f = None
    message = msg.payload.decode('utf-8')
    message = message.split('---')
    user_name = message[0]
    ecg_data = message[1]
    timestamp = message[2]
    print("Data: ", user_name, ecg_data)

    c.execute("SELECT * FROM users WHERE name=?", (user_name,))
    user = c.fetchone()
    if user == None:    
        c.execute("INSERT INTO users ('name') VALUES (?)", (user_name,))
        print("User does not exist, added to database.")
        user = c.lastrowid
        print("User: ", user)
        conn.commit()

    c.execute("SELECT * FROM users WHERE name=?", (user_name,))
    user = c.fetchone()
    print("User: ", user)
    data = ','.join(ecg_data)
    c.execute('''INSERT INTO data (user_id, message, timestamp) VALUES (?, ?, ?)''', (user[0], data, timestamp))
    conn.commit()



client.on_connect = on_connect
client.on_message = on_message
client.loop_start()

while True:
    pass




# 2^65536 | 2^8888
