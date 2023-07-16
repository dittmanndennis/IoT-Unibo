import logging
import asyncio
import time
import json

#from aiocoap import *
#from aiocoap.numbers.codes import GET

import paho.mqtt.client as mqtt_client

client = mqtt_client.Client()

#client.username_pw_set("iot2020", password="mqtt2020*")

client.connect("broker.hivemq.com", 1883, 60)

async def main():
    client.publish("unibo/iot/dennis/test", payload=json.dumps({ 'sampling_rate': 60, 'calibration': 300, 'alarm_level': 200, 'alarm_counter': 10 }))

    print("published")

    time.sleep(20)

if __name__ == "__main__":
    while True:
        asyncio.run(main())
