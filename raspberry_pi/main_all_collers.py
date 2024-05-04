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
    collorCounter = 0

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
				if os.stat(file_path_queue).st_size == 0:
					#apply vision
					[distanceBallYellow, distanceBallRed, distanceBallBlue, distanceGoalYellow, distanceGoalRed, distanceGoalBlue, angleGoalYellow, angleGoalRed, angleGoalBlue, angleBallYellow, angleBallRed, angleBallBlue] = Vision()
					print(str(angleBallYellow) + " " + str(distanceBallYellow) + "ball")
					print(str(angleGoalYellow) + " " + str(distanceGoalYellow) + "goal")
                    if collorCounter = 0:  # yellow
                        distanceBallCollor = distanceBallYellow
                        angleBallCollor = angleBallYellow
                        distanceGoalCollor = distanceGoalYellow
                        angleGoalCollor = angleGoalYellow
                        
                    elif collorCounter == 1: # blue
                        distanceBallCollor = distanceBallBlue
                        angleBallCollor = angleBallBlue
                        distanceGoalCollor = distanceGoalBlue
                        angleGoalCollor = angleGoalBlue
                    
                    else: # red
                        distanceBallCollor = distanceBallRed
                        angleBallCollor = angleBallRed
                        distanceGoalCollor = distanceGoalRed
                        angleGoalCollor = angleGoalRed
                                      
					if ballFunction == True:

						if (angleBallCollor == 0 and distanceBallCollor == 0):
							os.system("python send_to_arduino.py left 5 " + usb)
							counter = counter + 1
						else:
							distanceBallCollorPrev = distanceBallCollor
							counter = 0 
						action = ""
						if angleBallCollor < 0:
							angleBallCollorPrev = angleBallCollor
							action = "right"
						else: 
							angleBallCollorPrev = angleBallCollor
							action = "left"

						angleBallCollor = abs(angleBallCollor)
						distanceBallCollor = abs(distanceBallCollor)
						if angleBallCollor > 30: # ball is in left of camera
							if angleBallCollor > 45:
								angleBallCollor = 45
							angleBallCollor = np.int((angleBallCollor)/3)
							os.system("python send_to_arduino.py " + action + " " + str(angleBallCollor) + " "+ usb)
						elif angleBallCollor > 20: # ball is in left of camera
							if angleBallCollor > 45:
								angleBallCollor = 45
							angleBallCollor = np.int((angleBallCollor/2)/3)
							os.system("python send_to_arduino.py " + action + " " + str(angleBallCollor) + " "+ usb)	
						elif distanceBallCollor > 40 and angleBallCollor < 20:
							temp = 0	
							if distanceBallCollor > 45:
								os.system("python send_to_arduino.py forward 15 " + " "+ usb)
							else:
								os.system("python send_to_arduino.py forward " + str(np.int((distanceBallCollor/2)/3)) + " "+ usb)			
							dcounter = dcounter + 1	
						elif distanceBallCollor < 30 and angleBallCollor < 20 and angleBallCollor != 0:
							os.system("python send_to_arduino.py grab 1 "+ usb)
							print("grab 1")
							time.sleep(5)
							os.system("python send_to_arduino.py slide 1 "+ usb)
							time.sleep(5)
							print("slide 1")
							ballFunction = False
						else:
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

						if(angleBallCollor == 0 and distanceBallCollor == 0):
							os.system("python send_to_arduino.py left 5 " + usb)
							counterG = counterG + 1
						else:
							distanceBallCollorPrev = distanceBallCollor
							counterG = 0 
						action = ""
						if angleBallCollor < 0:
							angleBallCollorPrev = angleBallCollor
							action = "right"
						else: 
							angleBallCollorPrev = angleBallCollor
							action = "left"

						angleBallCollor = abs(angleBallCollor)
						distanceBallCollor = abs(distanceBallCollor)
						if angleBallCollor > 8: # ball is in left of camera
							if angleBallCollor > 45:
								angleBallCollor = 45
							angleBallCollor = np.int((angleBallCollor)/3)
							os.system("python send_to_arduino.py " + action + " " + str(angleBallCollor) + " "+ usb)
						elif distanceBallCollor > 130:
							temp = 0
							if distanceBallCollor > 45:
								temp = 45
							os.system("python send_to_arduino.py forward 5 "+ usb)

						elif distanceBallCollorPrev < 180 and angleBallCollor < 12 and angleBallCollor !=0:
							distanceBallCollor = np.int((distanceBallCollor)/3)
							
							os.system("python send_to_arduino.py grab 0 "+ usb)
							time.sleep(5)
							os.system("python send_to_arduino.py slide 0 "+ usb)
							time.sleep(5)
                            collorCounter = collorCounter + 1
                            if collorCounter > 2:
                                break
				else:
					with open(file_path_queue, 'r') as fin:
						data = fin.read().splitlines(True)
					with open(file_path_queue, 'w') as fout:
						fout.writelines(data[1:])
					#print(data[0])
					writeToCommandFile(hour_minute, "Raspberry Pi", "Action", data[0])
					os.system("sudo python send_to_arduino.py " + data[0].strip()  + " " + usb)

			fpsPrev = round(time.time() * 1000)
			print("fps:")
			print(str(fpsPrev-fpsNow))	
			wait = False