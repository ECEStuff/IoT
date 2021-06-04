import socket
import time
import adafruit_tcs34725
import busio
import digitalio
import board
import threading

def statusLED(): # only for thread to use to flash LED
    while(1):
        sigLED.value = True
        time.sleep(1)
        sigLED.value = False
        time.sleep(1)
        global isConn
        if isConn:
            break

# LEDs
sigLED = digitalio.DigitalInOut(board.D17)
RPiLED = digitalio.DigitalInOut(board.D27)
espLED = digitalio.DigitalInOut(board.D22)

sigLED.direction = digitalio.Direction.OUTPUT
RPiLED.direction = digitalio.Direction.OUTPUT
espLED.direction = digitalio.Direction.OUTPUT

# color sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_tcs34725.TCS34725(i2c)

HOST = '' 
PORT = 4120 # Port to listen on (non-privileged ports are > 1023)
isConn = False
lightThr = 1000 # light is assumed to be as bright as 1000 to get rid of outliers
dced = False

while(1): 
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((HOST, PORT))
    serverSocket.listen()
    isConn = False
    dced = False
    sendStr = ''

    # thread for the status LED
    t1 = threading.Thread(target = statusLED)
    t1.start()

    while (1):
        conn, addr = serverSocket.accept()
        if (addr != ''):
            print('RPi connected to ESP, now flashing LED faster')
            time.sleep(1)
            isConn = True
            t1.join()
                
            for i in range (0,8):
                print('flashing')
                sigLED.value = True
                time.sleep(0.25)
                sigLED.value = False
                time.sleep(0.25)
            print('done flashing')
        
        sigLED.value = True
        break;

    with conn:
        print('Connected by', addr)
        espSum = 0
        espAvg = 0
        RPiSum = 0
        RPiAvg = 0
        
        sendPerms = "You may send data."
        sendPerms = sendPerms.encode()
        conn.sendall(sendPerms)
        
        while(1):
            RPiSum = 0
            espSum = 0
            
            if (dced):
                break
            
            for i in range(0, 8):
                # ESP section
                data = conn.recv(1024)
                
                if not data:
                    print('end conn')
                    dced = True
                    break
                
                espRead = data.decode('utf-8')
                espNum = int(espRead) % lightThr
                print('ESP reading {}: {}'.format(i, espNum))
                espSum += espNum
                
                # RPi section
                RPiRead = sensor.lux % lightThr
                print('RPi reading {}: {}'.format(i, RPiRead))
                RPiSum += RPiRead
                time.sleep(.25) # wait 0.25 seconds to re-read sensor 
            
            RPiAvg = RPiSum/8
            espAvg = espSum/8
            print('RPi avg: {}'.format(RPiAvg))
            print('ESP avg: {}'.format(espAvg))
            
            if (RPiAvg >= espAvg): # RPi's value is greater
                RPiLED.value = True
                espLED.value = False
                sendStr = "RPi"
                sendStr = sendStr.encode()
                conn.sendall(sendStr)
            
            else: # ESP's value is less than
                RPiLED.value = False
                espLED.value = True
                sendStr = "ESP"
                sendStr = sendStr.encode()
                conn.sendall(sendStr)
            
            #if not data:
              #  print('end conn')
             #   break
                 
            #else: # connection
             #   print(sendStr)
                
             #   continue
    
    conn.close()
    serverSocket.close()
    RPiLED.value = False
    espLED.value = False
    sigLED.value = False