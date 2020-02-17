#!flask/bin/python

import sys

from flask import Flask, render_template, request, redirect, Response
from flask_cors import CORS
import random, json

from subprocess import Popen, PIPE 
import shlex
from threading import Thread

from Queue import Queue # Python 2

app = Flask(__name__)
CORS(app)

@app.route('/')
def output():
	# serve index template
	return render_template('dashboard.html', name='Joe')

@app.route('/receiver', methods=['POST'])
def worker():
	# read json + reply
	result = ""
	data = request.get_json()
	for item in data:
		result += str(data[item])
	output = run_command(result)
	return output

def run_command(command):

	def reader(pipe, queue):
		try:
			with pipe:
				for line in iter(pipe.readline, b''):
					queue.put((pipe, line))
		finally:
			queue.put(None)
			
	process = Popen(shlex.split(command), stdout=PIPE, stderr=PIPE, bufsize=1)
	q = Queue()
	Thread(target=reader, args=[process.stdout, q]).start()
	Thread(target=reader, args=[process.stderr, q]).start()
	
	
	
	def generate():
		result = ''
		for _ in range(2):
			for source, line in iter(q.get, None):
				yield line
				#print "%s: %s" % (source, line),

		"""
		while True:
			result = ""
			output = process.stdout.readline()
			if output:
				out = output.strip().decode('ascii')+"\n"
				result += out
			
			#error = process.stderr.readline()
			if error:
				out = error.strip().decode('ascii')+"\n"
				result += out
			
			if result == '' and process.poll() is not None:
				break

			if result != "":
				yield result
		"""
    #rc = process.poll()
	return Response(generate(),mimetype='text/csv')
if __name__ == '__main__':
	# run!
	app.run(host='localhost')
