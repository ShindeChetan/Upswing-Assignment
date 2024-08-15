import paho.mqtt.client as mqtt
import random
import time
import json

MQTT_BROKER = "localhost"
MQTT_PORT = 25672
MQTT_TOPIC = "status/update"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to MQTT broker")
    else:
        print(f"Failed to connect, return code {rc}")

def on_publish(client, userdata, mid):
    print(f"Message {mid} published.")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()

        while True:
            status = random.randint(0, 6)
            message = {"status": status}
            result = client.publish(MQTT_TOPIC, json.dumps(message))
            status_code = result.rc
            if status_code != 0:
                print(f"Failed to send message, return code {status_code}")
            else:
                print(f"Published message: {message}")
            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping MQTT client")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()