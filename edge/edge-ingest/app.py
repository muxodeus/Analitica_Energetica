import os, time, json
from pymodbus.client.sync import ModbusTcpClient
import paho.mqtt.client as mqtt

MB_HOST = os.getenv("MODBUS_HOST")
MB_PORT = int(os.getenv("MODBUS_PORT", 502))
MQTT_BROKER = os.getenv("MQTT_BROKER", "mosquitto")
MQTT_TOPIC  = os.getenv("MQTT_TOPIC", "energia/raw")

mqttc = mqtt.Client()
mqttc.connect(MQTT_BROKER, 1883, 60)

def read_and_publish():
    mb = ModbusTcpClient(MB_HOST, port=MB_PORT)
    if not mb.connect():
        print("Error: no se conecta a Modbus")
        return
    rr = mb.read_input_registers(0, 4)
    mb.close()
    if hasattr(rr, 'registers'):
        payload = {
            "ts": time.time(),
            "vals": rr.registers
        }
        mqttc.publish(MQTT_TOPIC, json.dumps(payload), qos=1)
        print("Publicado:", payload)

if __name__ == "__main__":
    while True:
        try:
            read_and_publish()
        except Exception as e:
            print("Error loop:", e)
        time.sleep(2)
