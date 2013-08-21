import pygame	# Used for Joystick
import math	# Used for tankdrive
import socket	# Used for client communications

def main():
	# Servos. Min, Max, Default
	DServo0 = [700,2200,1500] # DServo0 L/R: Left:700, Right: 2200 Center:1500 
	DServo1 = [700,2300,2300] # DServo1 TIlt: Backard: 700, Forward: 2300, Max: 2300
	DServo0Cur = DServo0[2]
	DServo1Cur = DServo1[2]

	# Initialize Joystick
	pygame.init() # Call Pygame
	j = pygame.joystick.Joystick(0) # j = Joystick 0
	j.init() # Initialize Joystick 0
	print "Initialized Joystick : %s" % j.get_name()

	# Initialize UDP connection
	#UDP_IP = "rover.helo.local"	# UDP Server
	UDP_IP = "192.168.43.141"
	UDP_PORT = 6005			# UDP Port
	sock = socket.socket(socket.AF_INET, # Internet
		socket.SOCK_DGRAM) # UDP
	bufferSize = 1024   # room for message

	# Initialize Relay States
	r0State = 0
	r1State = 0

	debounce = {}

	def _key_down(key, debounce_val=150):
		now = pygame.time.get_ticks()
		last = debounce.get(key, 0)
		if now - last > debounce_val:
			debounce[key] = now
			return True
		else:
			return False

	def _key_up(key):
		debounce[key] = 0

	def tankdrive(x,y): # Translated from JS @ goodrobot.com/en/2009/09/tank-drive-via-joystick-control
		z = math.sqrt(x*x + y*y)	# First hypotenuse
		if z == 0:			# Fix to prevent division by Zero
			z = 0.1			# (Set z=0.1)
		rad = math.acos(abs(x)/z)	# angle in radians
		angle = rad*180/math.pi		# and in degrees

		# Now angle indicates the measure of turn along a straight line,
		# with an angle o, the turn co-efficient is same.
		# This applies for angles between 0-90, with angle 0 the co-eff is -1
		# With angle 45, the co-efficient is 0 and with angle 90, it is 1
		tcoeff = -1 + (angle/90)*2
		turn = tcoeff * abs(abs(y) - abs(x))
		turn = round(turn*100)/100
		
		move = max(abs(y),abs(x))	# And max of y or x is the movement
		
		if (x >= 0 and y >= 0) or (x < 0 and  y < 0): # First and third quadrant
			left = move
			right = turn
		else:
			right = move
			left = turn
		
		if y < 0:
			left = 0 - left
			right = 0 - right

		if (left < 0):
			l_drive = 2
		else:
			l_drive = 0

		if (right < 0):
			r_drive = 2
		else:
			r_drive = 0

		return int(round(abs(left) * 250, 0)), l_drive, int(round(abs(right) * 250, 0)), r_drive

	while True:
		pygame.event.pump() # Process Pygame event handlers

		for i in range(0, j.get_numbuttons()):
			if j.get_button(i):
				if _key_down(i) is True:
					if i == 0:   # Button 1. Pan Left
						if DServo0Cur < DServo0[1]:
							DServo0Cur = DServo0Cur + 100
					elif i == 2: # Button 3. Pan Right
						if DServo0Cur > DServo0[0]:
							DServo0Cur = DServo0Cur - 100
					elif i == 1: # Button 2. Tilt Down
						if DServo1Cur < DServo1[1]:
							DServo1Cur = DServo1Cur + 100
					elif i == 3: # Button 4. Tilt Up
						if DServo1Cur > DServo1[0]:
							DServo1Cur = DServo1Cur - 100
					elif i == 9: # Button 9 (Start). Reset Pan/Tilt to Default
						DServo0Cur = DServo0[2]
						DServo1Cur = DServo1[2]
					elif i == 4: # Button 5 (Left Trigger 1). Switch Relay 0
						if r0State == 0:
							r0State = 1
						else:
							r0State = 0
					elif i == 5: # Button 6 (Right Trigger 1). Switch Relay 1
						if r1State == 0:
							r1State = 1
						else:
							r1State = 0
			else:
				_key_up(i)

		# Poll Joystick for X/Y cordinates
		x = j.get_axis(2) # Left/Right
		y = j.get_axis(1) # Forward/Reverse

		left, l_drive, right, r_drive = tankdrive(x,y) # Call tankdrive()

		if left <= 10 and right <= 10: # Stop motor squeal if speed <= 10.
			left = 0
			right = 0

		sock.sendto(bytes([r_drive, l_drive, right, left, DServo0Cur, DServo1Cur, r0State, r1State]), (UDP_IP, UDP_PORT))
		
		print(left,l_drive,right,r_drive,DServo0Cur,DServo1Cur,r0State,r1State)
		
		pygame.time.wait(10) # Sleep 10ms

if __name__ == "__main__":
    main()
    pygame.quit()
