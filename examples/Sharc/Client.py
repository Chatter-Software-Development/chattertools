import paho.mqtt.client as mqtt
import json
import uuid


class Client:
	def __init__(self, host: str, port: int, sharc_id: str):
		self._host = host
		self._port = port
		self._keepalive = 60
		self._sharc_id = sharc_id
		self._is_connected = False
		self._mqttc = mqtt.Client(client_id=f"id_{str(uuid.uuid4())}")
		self._cb_evt_avail = None
		self._cb_evt_ver = None
		self._cb_evt_rc = None
		self._cb_evt_net = None
		self._cb_evt_sensor = None
		self._cb_evt_mqtt = None
		self._cb_evt_user = None
		self._cb_evt_io_s0 = None
		self._cb_evt_io_s1 = None
		self._cb_evt_io_s2 = None
		self._cb_evt_io_s3 = None
		self._cb_evt_ack = None

	@property
	def is_connected(self):
		return self._is_connected

	def connect(self):
		self._mqttc.on_connect = self._on_connect
		self._mqttc.on_message = self._on_message
		self._mqttc.on_disconnect = self._on_disconnect
		self._mqttc.connect(host=self._host, port=self._port, keepalive=self._keepalive)
		self._mqttc.loop_start()

	def disconnect(self):
		self._mqttc.disconnect()
		self._mqttc.loop_stop(force=False)

	def _on_connect(self, client, userdata, flags, rc):
		self._is_connected = True if rc == 0 else False
		self._mqttc.subscribe(f"sharc/{self._sharc_id}/evt/#")

	def _on_message(self, client, userdata, message):
		segments = message.topic.split("/")
		event = segments[segments.index("evt") + 1]
		payload = json.loads(message.payload.decode("utf-8"))

		if event == "avail" and self._cb_evt_avail is not None:
			self._cb_evt_avail(payload["seq"], payload["v"])

		if event == "ver" and self._cb_evt_ver is not None:
			self._cb_evt_ver(payload["seq"], payload["v"])

		if event == "rc" and self._cb_evt_rc is not None:
			self._cb_evt_rc(payload["seq"], payload["v"])

		if event == "net" and self._cb_evt_net is not None:
			self._cb_evt_net(payload["seq"], payload["v"])

		if event == "sensor" and self._cb_evt_sensor is not None:
			self._cb_evt_sensor(payload["seq"], payload["v"])

		if event == "mqtt" and self._cb_evt_mqtt is not None:
			self._cb_evt_mqtt(payload["seq"], payload["v"])

		if event == "user" and self._cb_evt_user is not None:
			self._cb_evt_user(payload["seq"], payload["v"])

		if event == "io":
			if event == segments[-1]:
				if "s0" in payload["v"] and self._cb_evt_io_s0 is not None:
					self._cb_evt_io_s0(payload["seq"], payload["v"]["s0"])
				if "s1" in payload["v"] and self._cb_evt_io_s1 is not None:
					self._cb_evt_io_s1(payload["seq"], payload["v"]["s1"])
				if "s2" in payload["v"] and self._cb_evt_io_s2 is not None:
					self._cb_evt_io_s2(payload["seq"], payload["v"]["s2"])
				if "s3" in payload["v"] and self._cb_evt_io_s3 is not None:
					self._cb_evt_io_s3(payload["seq"], payload["v"]["s3"])
			else:
				sub_event = segments[segments.index(event) + 1]
				if sub_event == "s0" and self._cb_evt_io_s0 is not None:
					self._cb_evt_io_s0(payload["seq"], payload["v"])
				if sub_event == "s1" and self._cb_evt_io_s1 is not None:
					self._cb_evt_io_s1(payload["seq"], payload["v"])
				if sub_event == "s2" and self._cb_evt_io_s2 is not None:
					self._cb_evt_io_s2(payload["seq"], payload["v"])
				if sub_event == "s3" and self._cb_evt_io_s3 is not None:
					self._cb_evt_io_s3(payload["seq"], payload["v"])

		if event == "ack" and self._cb_evt_ack is not None:
			self._cb_evt_ack(payload["seq"], payload["v"])

	def _on_disconnect(self, client, userdata, rc):
		self._is_connected = False

	def request_io(self):
		if self.is_connected:
			payload = {"id": str(uuid.uuid4()), "v": {"io.publish": True}}
			self._mqttc.publish(f"sharc/{self._sharc_id}/cmd/action", json.dumps(payload))

	@property
	def on_available(self):
		return self._cb_evt_avail

	@on_available.setter
	def on_available(self, f):
		self._cb_evt_avail = f

	@property
	def on_version(self):
		return self._cb_evt_ver

	@on_version.setter
	def on_version(self, f):
		self._cb_evt_ver = f

	@property
	def on_reboot_count(self):
		return self._cb_evt_rc

	@on_reboot_count.setter
	def on_reboot_count(self, f):
		self._cb_evt_rc = f

	@property
	def on_network(self):
		return self._cb_evt_net

	@on_network.setter
	def on_network(self, f):
		self._cb_evt_net = f

	@property
	def on_sensor(self):
		return self._cb_evt_sensor

	@on_sensor.setter
	def on_sensor(self, f):
		self._cb_evt_sensor = f

	@property
	def on_mqtt(self):
		return self._cb_evt_mqtt

	@on_mqtt.setter
	def on_mqtt(self, f):
		self._cb_evt_mqtt = f

	@property
	def on_user(self):
		return self._cb_evt_user

	@on_user.setter
	def on_user(self, f):
		self._cb_evt_user = f

	@property
	def on_io_s0(self):
		return self._cb_evt_io_s0

	@on_io_s0.setter
	def on_io_s0(self, f):
		self._cb_evt_io_s0 = f

	@property
	def on_io_s1(self):
		return self._cb_evt_io_s1

	@on_io_s1.setter
	def on_io_s1(self, f):
		self._cb_evt_io_s1 = f

	@property
	def on_io_s2(self):
		return self._cb_evt_io_s2

	@on_io_s2.setter
	def on_io_s2(self, f):
		self._cb_evt_io_s2 = f

	@property
	def on_io_s3(self):
		return self._cb_evt_io_s3

	@on_io_s3.setter
	def on_io_s3(self, f):
		self._cb_evt_io_s3 = f

	@property
	def on_ack(self):
		return self._cb_evt_ack

	@on_ack.setter
	def on_ack(self, f):
		self._cb_evt_ack = f

