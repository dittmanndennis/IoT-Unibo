import logging
import asyncio
import time

from aiocoap import *
from aiocoap.numbers.codes import GET

import paho.mqtt.client as mqtt_client

logging.basicConfig(level=logging.INFO)

gas = []
alert = 0
delay_coap = []
delay_mqtt = []

async def main():
    global gas
    global alert
    global delay_coap
    global delay_mqtt

    protocol = await Context.create_client_context()

    request = Message(code=GET, uri='coap://130.136.2.70/time:5683')

    try:
        req_time = time.time()
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s\n%r'%(response.code, response.payload))
        
        delay_coap.append(time.time()-req_time)
        gas.append(float(response.payload))
        if float(response.payload) > 100:
            alert += 1
    
    if len(gas) == 20:
        print("Min: ", str(min(gas)), " Max: ", str(max(gas)), " Avg: ", str(sum(gas)/len(gas)))
        print("Avg delay_coap: ", str(sum(delay_coap)/len(delay_coap)))

        if alert > 3:
            pub_time = time.time()
            client.publish("sensor/alarm", payload='{"name": "Dennis", "mean": ' + str(sum(gas)/len(gas)) + ' }')
            delay_mqtt.append(time.time()-pub_time)
        else:
            pub_time = time.time()
            client.publish("sensor/regular", payload='{"name": "Dennis", "mean": ' + str(sum(gas)/len(gas)) + ' }')
            delay_mqtt.append(time.time()-pub_time)

        print("Avg delay_mqtt: ", str(sum(delay_mqtt)/len(delay_mqtt)))

        gas = []
        alert = 0
        delay_coap = []
        if len(delay_mqtt) == 20:
            delay_mqtt = []


    time.sleep(2)

client = mqtt_client.Client()

client.username_pw_set("iot2020", password="mqtt2020*")

client.connect("130.136.2.70", 1883, 60)

if __name__ == "__main__":
    while True:
        asyncio.run(main())
