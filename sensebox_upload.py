# Sensebox Upload
# Read CSV values from serial console and upload to opensensemap.org
# 2017 Stefan Teubner, Torsten Goerke

import time
from time import sleep
import serial
import requests
import json

serialPort = "/dev/ttyACM0"


milli_start = int(round(time.time() * 1000))

def initializeSerial(serPort):
        serialFound = False
        while (serialFound != True):
                try:
                        ser = serial.Serial(
                                port=serPort,
                                baudrate = 9600,
                                parity = serial.PARITY_NONE,
                                stopbits = serial.STOPBITS_ONE,
                                bytesize = serial.EIGHTBITS,
                                timeout = 0.5
                        )
                        serialFound = True
                except:
                        print "Serial-Port: "+serPort+" wurde nicht gefunden!"
                        serialFound = False
                sleep(0.5)
                return ser

ser = initializeSerial(serialPort)

counter = 0

def senseBoxUpload(boxID, sensorID, value):
        url = 'https://api.opensensemap.org/boxes/'+boxID+'/'+sensorID
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        payload = {'value': value}

        r = requests.post(url, data=json.dumps(payload), headers=headers)
        r.text
        r.status_code

try:
        while True:
                        # SERIAL WERTE AUSLESEN
                        valueCount = 0
                        while valueCount != 3:
                        #while 1:
                                line = ""
                                try:
                                        if(ser != 0):
                                                x=ser.readline()
                                                line = x.rstrip()
                                except:
                                        ser = initializeSerial(serialPort)
                                #print line
                                if(line != ""):
                                        if(counter < 3):
                                                print counter
                                                print "Startfilter ist aktiv."
                                                counter += 1
                                        else:
                                                values =line.split(",")
                                                valueCount = len(values)
                        a,b,c = values

                        print "Temperatur:  "+a+" \tLuftfeuchtigkeit: "+b+" \tTemperatur:  "+c+"\n"

                        # SENSEBOX UPLOAD
                        if((int(round(time.time() * 1000)) - milli_start) > 5000):
                                boxID="5947b313a4ad5900112e5ceb"
                                tempID = "5947bd17a4ad5900112ec9a7"
                                trueb1ID = "5947bdbba4ad5900112ed02c"
                                trueb2ID = "5947bdbba4ad5900112ed02d"
                                leitID = "5947bdbba4ad5900112ed02e"

                                senseBoxUpload(boxID,tempID, a)
                                senseBoxUpload(boxID,trueb1ID, b)
                                senseBoxUpload(boxID,trueb2ID, c)
                                #senseBoxUpload(boxID,leitID, leit)

except KeyboardInterrupt:
        ser.close()
