#For non-commercial use!

#Include libraries
import serial
import time
import re

posStringAnt = ''

#Define serial port
se = serial.Serial("/dev/ttyO2", 9600)
seGPS = serial.Serial("/dev/ttyO5", 4800)
#Regular expression to capture $GPGAA data
regex = re.compile("\$GPGGA,\S{10},(\d{2})(\S{7}),([NS]),(\d{3})(\S{7}),([EW]),([0126])")
#APN config.
se.write(bytes('AT+QIREGAPP="moviletb.net.co","etb","etb"\n','ASCII'))
#Wait for module to process the command (1 sec is ok)
time.sleep(1)
#Enable GPRS
se.write(bytes('AT+QIACT\n','ASCII'))
time.sleep(1)
#Connect module to the TCP server. Your IP goes here!
se.write(bytes('AT+QIOPEN="TCP","xxx.xxx.xxx.xxx","5000"\n','ASCII'))
time.sleep(1)

#Repeat during 30mins aprox.
for x in range(0, 7200):
	#This prevents that the process may die due to errors of serial sync
	try:
		line = seGPS.readline().decode("utf-8")
	#Allow ctrl+c
	except KeyboardInterrupt:
		seGPS.close()
		raise
	except:
		line = ""
		print("Serial sync error.")

	#If line is nor empty
	if line:
		#Regular expression matching
		res = regex.findall(line)
		res2 = regex.match(line)

		#If there are matches and GPS fix status is 1
		if res2 is not None and res[0][6] == '1':
			#Convert to decimal degrees coordinates
			pos = res[0]
			latNS = ""
			lonEW = ""
			if pos[2] == 'S':
				latNS = "-"
			if pos[5] == 'W':
				lonEW = "-"

			latDec = (float(pos[1]) / 60) + float(pos[0])
			lonDec = (float(pos[4]) / 60) + float(pos[3])

			#Six digits after the point
			latDec = "{:.6f}".format(latDec)
			lonDec = "{:.6f}".format(lonDec)

			#Make a string with lat. and lon. values
			posString = latNS + str(latDec) + "," + lonEW + str(lonDec)
			stringLen = len(posString)

			#Avoid to write twice the same coordinates
			if posString != posStringAnt:
				#Set buffer size to posString var length.
				se.write(bytes('AT+QISEND='+str(stringLen)+'\n','ASCII'))
				time.sleep(1)
				#Write the string to send it to the server.
				se.write(bytes(posString,'ASCII'))
				print(posString+"\n")
				time.sleep(1)
			posStringAnt = posString

time.sleep(1)
#Close connection
se.write(bytes('AT+QICLOSE\n','ASCII'))
time.sleep(1)
#Disable GPRS
se.write(bytes('AT+QIDEACT\n','ASCII'))
time.sleep(1)
#Close serial connection with the module
se.close()
seGPS.close()
