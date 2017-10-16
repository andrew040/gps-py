#!/usr/bin/env python
import serial
import string

ser = serial.Serial('/dev/ttyAMA0')  # open serial port
datavalid = 0
previous_time = 0

while True:
    file = open('/var/www/html/testfile.txt','a') 
    line = ser.readline() 

    if line[:6] == '$GPRMC':
        gprmcdata = line.split(',')
        gprmctime = gprmcdata[1]
        datavalid += 1

    if line[:6] == '$GPGGA':
        gpggadata = line.split(',')
        gpggatime = gpggadata[1]
        datavalid += 1

    if datavalid > 4:
     if gprmctime == gpggatime:
      if gpggatime != previous_time:
       print gprmcdata[9] + ' - ' + gprmcdata[1][:6]
       file.write(gprmcdata[1] + ',') # UTC time
       file.write(gprmcdata[2] + ',') # Fix valid
       file.write(gprmcdata[3] + ',') # latitude
       file.write(gprmcdata[4] + ',') # north/south
       file.write(gprmcdata[5] + ',') # longitude
       file.write(gprmcdata[6] + ',') # east/west
       file.write(gprmcdata[7] + ',') # speed
       file.write(gprmcdata[8] + ',') # true track
       file.write(gprmcdata[9] + ',') # date
       file.write(gpggadata[7] + ',') # number of satellites
       file.write(gpggadata[8] + ',') # hdop
       file.write(gpggadata[9]) # altitude
       file.write('\r\n')
       previous_time = gpggatime
    file.close()
ser.close()             # close port
