import sys
import serial
import time
import os
import datetime
import json
import numpy as np
from rasp_camera import Vision

def writeToCommandFile(time, fromm, type, content):
	a_dictionary = {"time": time, "from": fromm, "type":type, "content":content}

	with open("command_info.json", "r+") as file:
	    data = json.load(file)	# get data from file
	    #data = data.reverse()
	    data.append(a_dictionary)
	    #data = data.reverse()
	    file.seek(0)
	    json.dump(data, file)	# insert data in file

if __name__ == '__main__':
	line = "O"
	wait = True
	file_path_queue = "queue_info.txt"
	file_path_command = "command_info.txt"
	usb = '/dev/ttyACM0'
	ser = serial.Serial(usb, 38400, bytesize = serial.EIGHTBITS, parity = serial.PARITY_NONE, timeout=5)
	distanceBallYellowPrev = 0
	angleBallYellowPrev = 0
	distanceGoalYellowPrev = 0
	angleGoalYellowPrev = 0
	counter = 0
	counterG = 0 
	dcounter = 0
	ballFunction = True
	while(1):	
		while ser.inWaiting()==0: pass
		if  ser.inWaiting()>0:  
			line = ser.readline().decode('ascii').strip()
			now = datetime.datetime.now()
			hour = '{:02d}'.format(now.hour)
			minute = '{:02d}'.format(now.minute)
			second = '{:02d}'.format(now.second)
			fpsNow = round(time.time() * 1000)
			hour_minute = '{}.{}.{}'.format(hour, minute, second)
			if line == "O" and wait == False:
				writeToCommandFile(hour_minute, "Arduino", "Ready", "-")
				#print("yo")
				#print("ready" + line + "ready")
				if os.stat(file_path_queue).st_size == 0:
					#apply vision
					[distanceBallYellow, distanceBallRed, distanceBallBlue, distanceGoalYellow, distanceGoalRed, distanceGoalBlue, angleGoalYellow, angleGoalRed, angleGoalBlue, angleBallYellow, angleBallRed, angleBallBlue] = Vision()
					print(str(angleBallYellow) + " " + str(distanceBallYellow) + "ball")
					print(str(angleGoalYellow) + " " + str(distanceGoalYellow) + "goal")
					if ballFunction == True:
						if (angleBallYellow == 0 and distanceBallYellow == 0):
							os.system("python send_to_arduino.py left 5 " + usb)
							counter = counter + 1
						else:
							distanceBallYellowPrev = distanceBallYellow
							counter = 0 
						action = ""
						if angleBallYellow < 0:
							angleBallYellowPrev = angleBallYellow
							action = "right"
						else: 
							angleBallYellowPrev = angleBallYellow
							action = "left"

						angleBallYellow = abs(angleBallYellow)
						distanceBallYellow = abs(distanceBallYellow)
						if angleBallYellow > 30: # ball is in left of camera
							if angleBallYellow > 45:
								angleBallYellow = 45
							angleBallYellow = np.int((angleBallYellow)/3)
							os.system("python send_to_arduino.py " + action + " " + str(angleBallYellow) + " "+ usb)
						elif angleBallYellow > 20: # ball is in left of camera
							if angleBallYellow > 45:
								angleBallYellow = 45
							angleBallYellow = np.int((angleBallYellow/2)/3)
							os.system("python send_to_arduino.py " + action + " " + str(angleBallYellow) + " "+ usb)	
						elif distanceBallYellow > 40 and angleBallYellow < 20:
							temp = 0	
							if distanceBallYellow > 45:
								os.system("python send_to_arduino.py forward 15 " + " "+ usb)
							else:
								os.system("python send_to_arduino.py forward " + str(np.int((distanceBallYellow/2)/3)) + " "+ usb)			
							dcounter = dcounter + 1	
						elif distanceBallYellow < 30 and angleBallYellow < 20 and angleBallYellow != 0:
							print("555555")
							os.system("python send_to_arduino.py grab 1 "+ usb)
							print("grab 1")
							time.sleep(5)
							os.system("python send_to_arduino.py slide 1 "+ usb)
							time.sleep(5)
							print("slide 1")
							ballFunction = False
						else:
							print("666666")
							os.system("python send_to_arduino.py readsensor 3 " + usb)			

						if counter == 10 or dcounter == 1:
							print("counter " + str(counter) + " dcounter " + str(dcounter))
							os.system("python send_to_arduino.py grab 1 "+ usb)

							time.sleep(5)
							os.system("python send_to_arduino.py slide 1 "+ usb)
							time.sleep(5)

							ballFunction = False
					else:
						print("calculation goal")

						if(angleGoalYellow == 0 and distanceGoalYellow == 0):
							os.system("python send_to_arduino.py left 5 " + usb)
							counterG = counterG + 1
						else:
							distanceGoalYellowPrev = distanceGoalYellow
							counterG = 0 
						action = ""
						if angleGoalYellow < 0:
							angleGoalYellowPrev = angleGoalYellow
							action = "right"
						else: 
							angleGoalYellowPrev = angleGoalYellow
							action = "left"

						angleGoalYellow = abs(angleGoalYellow)
						distanceGoalYellow = abs(distanceGoalYellow)
						if angleGoalYellow > 8: # ball is in left of camera
							if angleGoalYellow > 45:
								angleGoalYellow = 45
							angleGoalYellow = np.int((angleGoalYellow)/3)
							os.system("python send_to_arduino.py " + action + " " + str(angleGoalYellow) + " "+ usb)
						elif distanceGoalYellow > 130:
							temp = 0
							if distanceGoalYellow > 45:
								temp = 45
							os.system("python send_to_arduino.py forward 5 "+ usb)

						elif distanceGoalYellowPrev < 180 and angleGoalYellow < 12 and angleGoalYellow !=0:
							distanceGoalYellow = np.int((distanceGoalYellow)/3)
							
							os.system("python send_to_arduino.py grab 0 "+ usb)
							time.sleep(5)
							os.system("python send_to_arduino.py slide 0 "+ usb)
							time.sleep(5)						
						
						else:
							os.system("python send_to_arduino.py readsensor 3 " + usb)			


				else:
					with open(file_path_queue, 'r') as fin:
						data = fin.read().splitlines(True)
					with open(file_path_queue, 'w') as fout:
						fout.writelines(data[1:])
					writeToCommandFile(hour_minute, "Raspberry Pi", "Action", data[0])
					os.system("sudo python send_to_arduino.py " + data[0].strip()  + " " + usb)

			fpsPrev = round(time.time() * 1000)
			print("fps:")
			print(str(fpsPrev-fpsNow))	
			wait = False