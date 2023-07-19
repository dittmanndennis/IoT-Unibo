import logging
import asyncio
import time

import requests as rq

from aiocoap import *
from aiocoap.numbers.codes import GET

from influxdb_client import InfluxDBClient

logging.basicConfig(level=logging.INFO)

async def main():
    temp = rq.get('http://130.136.2.70:8080/property/temp').json()["temp"]
    hum = rq.get('http://130.136.2.70:8080/property/hum').json()["hum"]

    protocol = await Context.create_client_context()

    request = Message(code=GET, uri='coap://130.136.2.70:5683')

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s\n%r'%(response.code, response.payload))
        gas = float(response.payload)
    
    print("Gas: ", gas)
    print("Temp: ", temp)
    print("Hum: ", hum)

    token = "0RZWMeMgRCXLBRCuSLZkPItZR2LpJ3SHq82pJ2QAJxBekaH_n0G_XmC_LPCymXvHeOiQjguZJBzoEJKB7639kg=="
    org = "iotclass"
    client = InfluxDBClient(url="http://130.136.2.70:9999", token=token, org=org)
    write_api = client.write_api()
    query_api = client.query_api()

    write_api.write("iotclass", "iotclass", [{"measurement": "tempValue", "tags": {"user": "Dennis"}, "fields": {"value": temp}}, {"measurement": "humValue", "tags": {"user": "Dennis"}, "fields": {"value": hum}}, {"measurement": "gasValue", "tags": {"user": "Dennis"}, "fields": {"value": gas}}])
    
    query = ' from(bucket:"iotclass")\
            |> range(start: -10m)\
            |> filter(fn: (r) => r._measurement == "tempValue")\
            |> filter(fn: (r) => r.user == "Dennis")\
            |> filter(fn: (r) => r._field == "value" )'
    result = query_api.query(org=org, query=query)

    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_value(), record.get_field()))

    print(results)

    time.sleep(20)

if __name__ == "__main__":
    while True:
        asyncio.run(main())

