#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, Response, jsonify
import os
import json
# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera
from random import randrange
app = Flask(__name__)

@app.route('/calculate_result')
def calculate_result():
	json_file_path = "command_info.json"
	m = 0;
	with open(json_file_path, 'r') as j:
	     data = json.loads(j.read())
	m=len(data)
	data4 = '<table > <colgroup> <col class=\"column_a\" /> <col class=\"column_b\" /> <col class=\"column_c\" /><col class="\column_d\" /></colgroup>'
	data4 = data4 + '<tr><th align=\"left\">Time</th><th align=\"left\">From</th><th align=\"left\">Type</th><th align=\"left"\>Content</th></tr><tr>'
	for k in range( m- 1, -1, -1):
		data4 = data4 + "<tr><td >" + data[k]['time'] + "</td><td >"+ data[k]['from']+ "</td><td >"+ data[k]['type']+"</td><td >"+data[k]['content']+"</td></tr>"
	data4=data4+"</table>"	
	data2=[ 'first'  ]
	data3 = "<ul style=\"list-style-type:none\" >"
	with open("queue_info.txt", "r") as a_file:
		for line in a_file:
			stripped_line = line.strip()
			data2.insert(0,stripped_line)
	for i in range( len(data2) - 1):
		data3 = data3 + "<li>" + str(data2[i]) + "</li>"
	data3 = data3 + "</ul>"
	return jsonify({"data2":data3, "result":randrange(100), "data4":data4})

@app.route('/', methods=['POST'])
def my_form_post():
	distance = 0
	if request.method == 'POST':
		file = open("queue_info.txt","a")
		if request.form['submit_forward'] == 'Forward':
			distance = int(int(request.form['stopDistance'])/3)
			if distance > 15:
				distance = 15
			if distance < 1:
				distance = 1
			file.write("forward " + str(distance) + "\n")
		elif request.form['submit_forward'] == 'Stop':
			file.write("stop\n")
		elif request.form['submit_forward'] == 'Left':
			distance = int(int(request.form['stopDistance'])/3)
			if distance > 15:
				distance = 15
			if distance < 1:
				distance = 1
			file.write("left " + str(distance) + "\n")
		elif request.form['submit_forward'] == 'Right':
			distance = int(int(request.form['stopDistance'])/3)
			if distance > 15:
				distance = 15
			if distance < 1:
				distance = 1
			file.write("right " + str(distance) + "\n")
		elif request.form['submit_forward'] == 'Grab':
			distance = int(request.form['stopDistance'])
			if distance > 1:
				distance = 1
			if distance < 0:
				distance = 0
			file.write("grab " + str(distance) + "\n")
		elif request.form['submit_forward'] == 'Slide':
			distance = int(request.form['stopDistance'])
			if distance > 1:
				distance = 1
			if distance < 0:
				distance = 0
			file.write("slide " + str(distance) + "\n")
		elif request.form['submit_forward'] == 'Sens 1 cur':
			file.write("readsensor 0\n")
		elif request.form['submit_forward'] == 'Sens 2 cur':
			file.write("readsensor 1\n")
		elif request.form['submit_forward'] == 'Sens 1 vol':
			file.write("readsensor 2\n")
		elif request.form['submit_forward'] == 'Sens 2 vol':
			file.write("readsensor 3\n")
		elif request.form['submit_forward'] == 'Sens 1 pwr':
			file.write("readsensor 4\n")
		elif request.form['submit_forward'] == 'Sens 2 pwr':
			file.write("readsensor 5\n")
		file.close()
	json_file_path = "command_info.json"
	with open(json_file_path, 'r') as j:
	     data = json.loads(j.read())
	data2=[ { 'name':'first' } ]
	with open("queue_info.txt", "r") as a_file:
		for line in a_file:
			stripped_line = line.strip()
			data2.insert(0,{'name':stripped_line})

	templateData = {
	'stopDistance': distance,
	'data':data, 'data2':data2
	}
	return render_template('index.html', **templateData)

@app.route("/<command>")
def move(command):
	global globalCommand
	global status
	file = open("queue_info.txt","a")
	if command == 'forwards':
		file.write("Moveforwards\n")
	if command == 'backwards':
		file.write("Move backwards\n")
	if command == 'left':
		file.write("Move left\n")
	if command == 'right':
		file.write("Move right\n")
	if command == 'stop':
		file.write("Stop\n")
	file.close()
	
	json_file_path = "command_info.json"
	with open(json_file_path, 'r') as j:
	     data = json.loads(j.read())
	data2=[ { 'name':'first' } ]
	with open("queue_info.txt", "r") as a_file:
		for line in a_file:
			stripped_line = line.strip()
			data2.insert(0,{'name':stripped_line})
	return render_template('index.html', data=data, data2=data2)


@app.route('/')
def index():
	"""Video streaming home page."""
	json_file_path = "command_info.json"
	global distance;
	with open(json_file_path, 'r') as j:
		data = json.loads(j.read())
	data2=[ { 'name':'first' } ]
	with open("queue_info.txt", "r") as a_file:
		for line in a_file:
			stripped_line = line.strip()
			data2.insert(0,{'name':stripped_line})
	return render_template('index.html', data=data, data2=data2)

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    camera = Camera()
    camera.vflip = True
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port =8080, debug=True, threaded=True)
