import network,time
from simple import MQTTClient #导入MQTT板块
from machine import I2C,Pin,Timer
from lsm6dsox import LSM6DSOX

from machine import Pin, I2C
lsm = LSM6DSOX(I2C(0, scl=Pin(13), sda=Pin(12)))

def WIFI_Connect():
    wlan = network.WLAN(network.STA_IF) #STA模式
    wlan.active(True)                   #激活接口
    start_time=time.time()              #记录时间做超时判断

    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('olleh_WiFi_37D2', '0000009850') #输入WIFI账号密码
        
    if wlan.isconnected():
        print('network information:', wlan.ifconfig())
        return True    

def MQTT_Send(tim):
    global lsm
    client.publish(TOPIC, '{}'.format(round(lsm.read_gyro()[2])))
    print('{}'.format(round(lsm.read_gyro()[2])))
    
if WIFI_Connect():
    SERVER = '172.30.1.39'   #my rapa ip address , mqtt broker가 실행되고 있음
    PORT = 1883
    CLIENT_ID = '' # clinet id 이름
    TOPIC = 'test' # TOPIC 이름
    client = MQTTClient(CLIENT_ID, SERVER, PORT, keepalive=30)
    client.connect()

    #开启RTOS定时器，编号为-1,周期1000ms，执行socket通信接收任务
    tim = Timer(-1)
    tim.init(period=1000, mode=Timer.PERIODIC,callback=MQTT_Send)
