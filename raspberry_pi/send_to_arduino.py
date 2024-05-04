import sys
import serial
import time
import numpy as np
import datetime
import json

def writeToCommandFile(time, fromm, type, content):
	a_dictionary = {"time": time, "from": fromm, "type":type, "content":content}

	with open("command_info.json", "r+") as file:
	    data = json.load(file)	# get data from file
	    data.append(a_dictionary)
	    #data = data.reverse()
	    file.seek(0)
	    json.dump(data, file)	# insert data in file

def sendCmd(cmd, receive, usb): 
	ser = serial.Serial(usb, 38400, bytesize = serial.EIGHTBITS, parity = serial.PARITY_NONE, stopbits=1, timeout=5)
	cmd2 = chr(cmd)
	ser.write(cmd2[0].encode())
	arr = ""
	print(cmd2[0].strip().encode())
	while(True):
		while ser.inWaiting()==0: pass
		if  ser.inWaiting()>0:  
			line = ser.readline().decode('ascii').rstrip()
			arr = line
	return arr;

if __name__ == '__main__':
	action = (sys.argv[1])
	value = np.int8(sys.argv[2])
	usb = sys.argv[3]
	cmd = 0

	if action == "right":
        	cmd = (value << 3) | 0x03
        	sendCmd(cmd, False, usb)
	elif action == "slide":
        	cmd = (value << 3) | 0x01
        	sendCmd(cmd, False, usb)
	elif action == "forward":
        	cmd = (value << 3) | 0x02
        	print("{0:b}".format(cmd))
        	sendCmd(cmd, False, usb)
        	#print("forward " + returnVal)
	elif action == "left":
        	cmd = (value << 3) | 0x04
        	returnVal =  sendCmd(cmd, False, usb)
        	print("forward " + returnVal)
	elif action == "readsensor":
			now = datetime.datetime.now()
			hour = '{:02d}'.format(now.hour)
			minute = '{:02d}'.format(now.minute)
			second = '{:02d}'.format(now.second)
			hour_minute = '{}.{}.{}'.format(hour, minute, second)
			cmd = (value << 3) | 0x05
			print("{0:b}".format(cmd))
			returnVal = sendCmd(cmd, True, usb)
			if(value == 0):
				print("current sensor 1: " + returnVal)
				writeToCommandFile(hour_minute, "Arduino", "Response", returnVal + " mA")
			elif(value == 1):
				print("current sensor 2: " + returnVal)
				writeToCommandFile(hour_minute, "Arduino", "Response", returnVal + " mA")
			elif(value == 2):
				print("voltage sensor 1: " + returnVal)
				writeToCommandFile(hour_minute, "Arduino", "Response", returnVal + " V")
			elif(value == 3):
				print("voltage sensor 2: " + returnVal)
				writeToCommandFile(hour_minute, "Arduino", "Response", returnVal + " V")
			elif(value == 4):
				print("power sensor 1: " + returnVal)
				writeToCommandFile(hour_minute, "Arduino", "Response", returnVal + " mW")
			elif(value == 5):
				print("power sensor 1: " + returnVal)
				writeToCommandFile(hour_minute, "Arduino", "Response", returnVal + " mW")
	elif action == "grab":
			cmd = (value << 3 | 0x06)
			sendCmd(cmd, False, usb)
