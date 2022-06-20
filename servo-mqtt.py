import random
from socket import MsgFlag
import time
import paho.mqtt.client as mqtt_client
import sys
import time
from pymata4 import pymata4

broker_address = "localhost"
broker_port = 1883

topic = "test"


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker")
        else:
            print(f"Failed to connect, Returned code: {rc}")

    def on_disconnect(client, userdata, flags, rc=0):
        print(f"disconnected result code {str(rc)}")

    def on_log(client, userdata, level, buf):
        print(f"log: {buf}")

    # client 생성
    client_id = f"mqtt_client_{random.randint(0, 1000)}"
    client = mqtt_client.Client(client_id)

    # 콜백 함수 설정
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_log = on_log

    # broker 연결
    client.connect(host=broker_address, port=broker_port)
    return client

angle = 90

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global angle
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if int(msg.payload.decode()) > 0: angle += 10
        elif int(msg.payload.decode()) < 0: angle -= 10
        elif msg.payload.decode() == msg.payload.decode(): angle = angle
            
        try:
            servo(board, 11, angle)
        except KeyboardInterrupt:
            board.shutdown()
            sys.exit(0)
            
    client.subscribe(topic) #1
    client.on_message = on_message
def servo(my_board, pin, angle):
    my_board.set_pin_mode_servo(pin)
    my_board.servo_write(pin, angle)
    time.sleep(1)
board = pymata4.Pymata4()

def run():
    client = connect_mqtt()
    subscribe(client)

    client.loop_forever()
    
    
if __name__ == '__main__':
    run()
