import os
from Client import Client as SharcClient
import chattertools as ch
from dotenv import load_dotenv
import time
load_dotenv()
SHARC_ID = "409151d72b80"
MQTT_HOST = "wss.sharc.tech"
SHARC_SENSOR = "s3"
MACHINE_ID = 5187
MQTT_PORT = 1883
CHATTER_KEY = os.getenv('CHATTER_API_KEY')
def print_sharc_event(note, sequence, message):
    print(f"[sharc:{SHARC_ID}] [sequence:{sequence}] {note} {message}")


def send_air_pressure(message):
    chatter = ch.Client(key=CHATTER_KEY)
    test_machine = chatter.machines.get(MACHINE_ID)
    transaction = test_machine.transactions.create(None, ch.DataType.AIR_PRESSURE, message[SHARC_SENSOR]["v"])
    print(transaction)



sharc = SharcClient(MQTT_HOST, MQTT_PORT, SHARC_ID)


# example payload
# send_air_pressure({SHARC_SENSOR: {"u": "count", "v": 20}})

sharc = SharcClient(MQTT_HOST, MQTT_PORT, SHARC_ID)
sharc.on_available = lambda sequence, message: print_sharc_event("Is Available:", sequence, message)
sharc.on_version = lambda sequence, message: print_sharc_event("Version:", sequence, message)
sharc.on_reboot_count = lambda sequence, message: print_sharc_event("Reboot Count:", sequence, message)
sharc.on_network = lambda sequence, message: print_sharc_event("Network:", sequence, message)
sharc.on_sensor = lambda sequence, message: print_sharc_event("Sensor:", sequence, message)
sharc.on_mqtt = lambda sequence, message: print_sharc_event("MQTT:", sequence, message)
sharc.on_user = lambda sequence, message: print_sharc_event("User:", sequence, message)
sharc.on_io_s0 = lambda sequence, message: print_sharc_event("S0:", sequence, message)
sharc.on_io_s0 = lambda sequence, message: send_air_pressure(message)
sharc.on_io_s1 = lambda sequence, message: print_sharc_event("S1:", sequence, message)
sharc.on_io_s1 = lambda sequence, message: send_air_pressure(message)
sharc.on_io_s2 = lambda sequence, message: print_sharc_event("S2:", sequence, message)
sharc.on_io_s2 = lambda sequence, message: send_air_pressure(message)
sharc.on_io_s3 = lambda sequence, message: print_sharc_event("S3:", sequence, message)
sharc.on_io_s3 = lambda sequence, message: send_air_pressure(message)
sharc.on_ack = lambda sequence, message: print_sharc_event("Ack:", sequence, message)
sharc.connect()
print(SHARC_ID + ' connected')

while True:
	choice = input()
	choice = choice.lower()

	if choice == 'io':
		sharc.request_io()
