#Include libraries
import serial
import time

#Define serial port
se = serial.Serial("/dev/ttyO2", 9600)
#APN config.
se.write(bytes('AT+QIREGAPP="moviletb.net.co","etb","etb"\n','ASCII'))
#Wait for module to process the command (1 sec is ok)
time.sleep(1)
#Enable GPRS
se.write(bytes('AT+QIACT\n','ASCII'))
time.sleep(1)
#Connect module to the TCP server
se.write(bytes('AT+QIOPEN="TCP","xxx.xxx.xxx.xxx","5000"\n','ASCII'))

#Repeat 4 times
for i in range(1, 5):
	#Get actual time
	now = time.localtime(time.time())
	#Make string with hours, minutes and seconds
	timeString = time.strftime("%H:%M:%S",now)
	time.sleep(1)
	#Set buffer size to 30 chars.
	se.write(bytes('AT+QISEND=30\n','ASCII'))
	time.sleep(1)
	#Write 30 chars to send to the TCP server
	se.write(bytes(timeString + ' UTC: Hi. I am alive!\n','ASCII'))
time.sleep(1)
#Close connection
se.write(bytes('AT+QICLOSE\n','ASCII'))
time.sleep(1)
#Disable GPRS
se.write(bytes('AT+QIDEACT\n','ASCII'))
time.sleep(1)
#Close serial connection with the module
se.close()