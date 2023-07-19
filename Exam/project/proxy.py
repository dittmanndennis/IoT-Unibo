import logging
import asyncio

from constants import INFLUXDB, MQTT_BROKER

import aiocoap
import aiocoap.resource as resource
import paho.mqtt.client as mqtt_client
from influxdb_client import InfluxDBClient


class DataResource(resource.Resource):
    async def render_post(self, request):
        payload = request.payload.decode()
        alarm, weight, temp, hum, rssi = payload.split(", ")
        print("Data POST payload: ", payload)

        record = [
                    {
                        "measurement": "weight",
                        "tags": {
                            "alarm": alarm == "True"
                            },
                        "fields": {
                            "value": float(weight)
                        }
                    },
                    {
                        "measurement": "temp",
                        "fields": {
                            "value": float(temp)
                            }
                    },
                    {
                        "measurement": "hum",
                        "fields": {
                            "value": float(hum)
                            }
                    },
                    {
                        "measurement": "rssi",
                        "fields": {
                            "value": float(rssi)
                            }
                    }
                ]
        write_api.write(INFLUXDB['TEST_BUCKET'], INFLUXDB['ORG'], record)

        return aiocoap.Message(code=aiocoap.CHANGED, payload=b"True")
    
class ConfigResource(resource.Resource):
    async def render_post(self, request):
        print("Config POST payload: ", request.payload.decode())

        #sampling_rate, calibration, alarm_level, alarm_counter
        client.publish(MQTT_BROKER['TOPIC'], payload=request.payload)

        return aiocoap.Message(code=aiocoap.CHANGED, payload=b"True")

class WhoAmI(resource.Resource):
    async def render_get(self, request):
        text = ["Used protocol: %s." % request.remote.scheme]

        text.append("Request came from %s." % request.remote.hostinfo)
        text.append("The server address used %s." % request.remote.hostinfo_local)

        claims = list(request.remote.authenticated_claims)
        if claims:
            text.append("Authenticated claims of the client: %s." % ", ".join(repr(c) for c in claims))
        else:
            text.append("No claims authenticated.")

        return aiocoap.Message(content_format=0,
                payload="\n".join(text).encode('utf8'))


# logging setup

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

# mqtt setup

client = mqtt_client.Client()
client.connect(MQTT_BROKER['HOST'], MQTT_BROKER['TCP_PORT'], 60)

## influxdb setup

write_api = InfluxDBClient(url=INFLUXDB['URL'], token=INFLUXDB['TOKEN'], org=INFLUXDB['ORG']).write_api()

async def main():
    # Resource tree creation
    root = resource.Site()
    print(root)

    root.add_resource(['.well-known', 'core'],
            resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(['whoami'], WhoAmI())
    root.add_resource(['data'], DataResource())
    root.add_resource(['config'], ConfigResource())

    # bind to machine network address (MacOs: ifconfig - status: active)
    await aiocoap.Context.create_server_context(bind=('192.168.2.177',5683), site=root)

    # Run forever
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())

