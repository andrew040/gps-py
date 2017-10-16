#!/usr/bin/env python
import serial
import string

ser = serial.Serial('/dev/ttyAMA0')  # open serial port
datavalid = 0
previous_time = 0

key = open('key','r')
last_key = int(key.read())
last_key += 1
key.close()

key = open('key','w')
key.write(str(last_key))
key.close()

file = open('/var/www/html/testfile'+str(last_key)+'.txt','w')

file.write('<gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">\n')
file.write('  <trk>\n')
file.write('    <name>GPX Track</name>\n')
file.write('    <trkseg>\n')

file.close()

print('File: '+str(last_key))
while True:
    file = open('/var/www/html/testfile'+str(last_key)+'.txt','a') 
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
       atomtime = '20'+gprmcdata[9][4:6]+'-'+gprmcdata[9][2:4]+'-'+gprmcdata[9][0:2]+'T'
       atomtime = atomtime + gprmcdata[1][:2]+':'+ gprmcdata[1][2:4]+':'+ gprmcdata[1][4:6]+'Z'
       latdeg = gprmcdata[3][:2]
       latdec = gprmcdata[3][2:]
       lat = float(latdeg)+float(latdec)/60

       londeg = gprmcdata[5][:3]
       londec = gprmcdata[5][3:]
       if gprmcdata[6]=='W':
        londeg = float(londeg) * -1
        lon = float(londeg)-float(londec)/60
       else:
        lon = float(londeg)+float(londec)/60

       file.write('      <trkpt lat="'+str(lat)+'" lon="'+str(lon)+'">\n')
       file.write('        <ele>'+gpggadata[9]+'</ele>\n')
       file.write('        <time>'+atomtime+'</time>\n')
       file.write('        <hdop>'+gpggadata[8]+'</hdop>\n')
       file.write('        <sat>'+gpggadata[7]+'</sat>\n')
       file.write('        <geoidheight>'+gpggadata[11]+'</geoidheight>\n')
       file.write('      </trkpt>\n')
       previous_time = gpggatime
    file.close()
ser.close()             # close port
