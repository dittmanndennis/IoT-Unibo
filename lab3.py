import logging
import asyncio
import time

import requests as rq

from aiocoap import *
from aiocoap.numbers.codes import GET

logging.basicConfig(level=logging.INFO)

gas = []
temp = []
hum = []

async def main():
    global gas
    global temp
    global hum

    temp.append(rq.get('http://130.136.2.70:8080/property/temp').json()["temp"])
    hum.append(rq.get('http://130.136.2.70:8080/property/hum').json()["hum"])

    protocol = await Context.create_client_context()

    request = Message(code=GET, uri='coap://130.136.2.70:5683')

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s\n%r'%(response.code, response.payload))
        gas.append(float(response.payload))
    
    if len(temp) == 6:
        print("Avg Gas: ", str(sum(gas)/len(gas)))
        print("Avg Temp: ", str(sum(temp)/len(temp)))
        print("Avg Hum: ", str(sum(hum)/len(hum)))

        res = rq.get("https://api.thingspeak.com/update?api_key=GAXDS0Y7VCM9NTR7&field1="+str(sum(gas)/len(gas))+"&field2="+str(sum(temp)/len(temp))+"&field3="+str(sum(hum)/len(hum)))
        print("Response: "+str(res.json()))

        gas = []
        temp = []
        hum = []

    time.sleep(5)

if __name__ == "__main__":
    while True:
        asyncio.run(main())

