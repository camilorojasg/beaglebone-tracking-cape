#Used libraries
import re
import serial

#Open serial port
ser = serial.Serial("/dev/ttyO5", 4800)
posStringAnt = ""

#Regular expression to capture $GPGAA data
regex = re.compile("\$GPGGA,\S{10},(\d{2})(\S{7}),([NS]),(\d{3})(\S{7}),([EW]),([0126])")

#Infinite loop
while True:
	#This prevents that the process may die due to errors of serial sync
	try:
		line = ser.readline().decode("utf-8")
	#Allow ctrl+c
	except KeyboardInterrupt:
		ser.close()
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
			posString = latNS + str(latDec) + "," + lonEW + str(lonDec) + "\n"

			#Avoid to write twice the same coordinates
			if posString != posStringAnt:
				#Write string to a file (append mode)
				with open("/home/debian/trackingCape/test.txt", "a") as logFile:
					logFile.write(posString)
					logFile.close()
			posStringAnt = posString
