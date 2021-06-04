import socket
import time
import adafruit_tcs34725
import busio
import digitalio
import board
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("ESP")
    
def on_message(client, userdata, msg):
    print("Topic: {}, ESP reading: {}".format(msg.topic, str(msg.payload.decode("UTF-8"))))
    
    # ESP
    espRead = msg.payload.decode('utf-8')
    espNum = int(espRead) % lightThr # correct outliers
    print("ESP: {}".format(espNum))
    
    #RPi
    RPiRead = sensor.lux % lightThr
    print("RPi: {}".format(RPiRead))
        
    if(RPiRead >= espNum): 
        sendStr = ("RPi: {}".format(RPiRead))
        client.publish("iot", sendStr)
            
    else:
        sendStr = ("ESP: {}".format(espRead))
        client.publish("iot", sendStr)

# color sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_tcs34725.TCS34725(i2c)
lightThr = 2000 # light is assumed to be as bright as 1000 to get rid of outliers

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

broker_address = "127.0.0.1"
PORT = 1883 # MQTT port

client.connect(broker_address, PORT, 60)
client.loop_forever()