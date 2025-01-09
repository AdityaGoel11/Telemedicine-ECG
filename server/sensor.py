import paho.mqtt.publish as publish
import csv
import time

host = "localhost"
port = 1883

user_name = "user1"

with open('ecgsample.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data = '---'.join(row)
        print(data)
        publish.single("sensor", data, hostname=host, port=port)
        time.sleep(0.1)

