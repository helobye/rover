#!/usr/bin/env python

import sys    # Used for script args
import smbus  # Used for i2c
import socket # Used for client communications
import piface.pfio as pfio # Used for relays/switches
from daemon import Daemon

class rover_svc(Daemon):
	def run(self):
		# Initialize UDP connection
		UDP_IP = "192.168.1.10" # UDP Server
		UDP_PORT = 6005		# UDP Port
		sock = socket.socket(socket.AF_INET, # Internet
		socket.SOCK_DGRAM) # UDP
		sock.bind((UDP_IP, UDP_PORT))
		
		# Initialize i2c
		bus = smbus.SMBus(1) # RPi rev 2 = SMBus(1)
		device = 0x04 # Arduino i2c device address
		
		# Initialize Piface IO
		pfio.init()
		r0 = pfio.Relay(0)
		r0State = 0
		r0CurState = 0
		r1 = pfio.Relay(1)
		r1State = 0
		r1CurState = 0
		
		while True:
			print "Listening"
			recv_data, addr = sock.recvfrom(1024)
			recv_data = recv_data.strip('[]').split(',')
			recv_data = [int(x) for x in recv_data]
			r_drive = recv_data[0]
			l_drive = recv_data[1]
			right = recv_data[2]
			left = recv_data[3]
			DServo0Cur = recv_data[4]
			DServo1Cur = recv_data[5]
			r0State = recv_data[6]
			r1State = recv_data[7]

			print r_drive, l_drive, right, left, DServo0Cur, DServo1Cur, r0State, r0CurState, r1State, r0CurState
        
			if r0State != r0CurState:
				if r0State == 1:
					r0.turn_on()
					r0CurState = 1
				else:
					r0.turn_off()
					r0CurState = 0
        
			if r1State != r1CurState:
				if r1State == 1:
					r1.turn_on()
					r1CurState = 1
				else:
					r1.turn_off()
					r1CurState = 0

			try:
				bus.write_i2c_block_data(device, 1, [r_drive, l_drive, right, left, DServo0Cur/10, DServo1Cur/10])
			except IOError, err:
					print "Lost I2C"

if __name__ == "__main__":
	daemon = rover_svc('/tmp/rover.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
