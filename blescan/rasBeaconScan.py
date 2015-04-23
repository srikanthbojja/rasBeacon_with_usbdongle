# BLE Scanning software
# GoldBassist from www.rasplay.org 4/23/2015
# Thanx to 
# https://github.com/adamf
# https://github.com/switchdoclabs/iBeacon-Scanner-
# and
# Bluez

import blescan
import sys
import RPi.GPIO as GPIO
import time

import bluetooth._bluetooth as bluez

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

p = GPIO.PWM(23,50) #set the PWM on pin 23 to 50percent
p.start(0)

####
# getDistance is not good.
####
def getDistance(rssi, txPower):
        #
        # RSSI = TxPower - 10 * n * lg(d)
        # n = 2 (in free space)
        #
        # d = 10 ^ ((TxPower - RSSI) / (10 * n))
        return pow(10, (txPower-rssi)/(10*2))

dev_id = 0
try:
        sock = bluez.hci_open_dev(dev_id)
        print "ble thread started"

except:
        print "error accessing bluetooth device..."
        sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

while True:
        rssi = 0
        txPower = 0
        distance = 0

        returnedList = blescan.parse_events(sock, 10)
        for beacon in returnedList:
                #print beacon
                row = beacon.split(',')
                
                # Change row[1] value to your beacon ID
                if row[1]=='e20a39f473f54bc4a12f17d1ad07a961' or row[1]=='65ffdf36bc6a42b6b3709674342abbbb':
                #if True:
                        txPower = abs(int(row[4]))
                        rssi = abs(int(row[5]))
                        distance = getDistance(rssi, txPower)
                        #print ('%s tx:%d rssi:%d distance:%d' % (row[1], txPower, rssi, distance))
                        #print ('distance:%d' % distance)
                        if rssi != 40:
                                value = ((100.0-rssi)/(100-40))*100
                                if value>100:
                                        value = 100
                                if value<0:
                                        value = 0
                                p.ChangeDutyCycle(value)
                                zonename = ''
                                
                                # Change row[1] value to your beacon ID
                                if row[1]=='e20a39f473f54bc4a12f17d1ad07a961':
                                        zonename = 'rasppizone'
                                elif row[1]=='65ffdf36bc6a42b6b3709674342abbbb':
                                        zonename = 'iphonezone'
                                #print ('%s tx:%d rssi:%d value:%f' % (row[1], txPower, rssi, value))
                                print ('%s tx:%d rssi:%d value:%f' % (zonename, txPower, rssi, value))
                                time.sleep(0.02)

GPIO.cleanup()
