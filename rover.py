import pygame	# Used for Joystick
import time	# Used for Sleep
import smbus	# Used for i2c
import math	# Used for tankdrive

bus = smbus.SMBus(1) # RPi rev 2 = SMBus(1)

device = 0x04 # Arduino i2c device address

# Servos. Min, Max, Default
DServo0 = [700,2200,1500] # DServo0 L/R: Left:700, Right: 2200 Center:1500 
DServo1 = [700,2300,2300] # DServo1 TIlt: Backard: 700, Forward: 2300, Max: 2300
DServo0Cur = DServo0[2]
DServo1Cur = DServo1[2]

pygame.init() # Call Pygame
j = pygame.joystick.Joystick(0) # j = Joystick 0
j.init() # Initialize Joystick 0
print 'Initialized Joystick : %s' % j.get_name()

def tankdrive(x,y): # Converted from JS found here: goodrobot.com/en/2009/09/tank-drive-via-joystick-control
	z = math.sqrt(x*x + y*y)	# First hypotenuse
	if z == 0: # Fix to prevent division by Zero
		z = 0.1
	rad = math.acos(abs(x)/z)	# angle in radians
	angle = rad*180/math.pi		# and in degrees

	# Now angle indicates the measure of turn along a straight line,
	# with an angle o, the turn co-efficient is same.
	# This applies for angles between 0-90, with angle 0 the co-eff is -1
	# With angle 45, the co-efficient is 0 and with angle 90, it is 1
	tcoeff = -1 + (angle/90)*2
	turn = tcoeff * abs(abs(y) - abs(x))
	turn = round(turn*100)/100
	
	move = max(abs(y),abs(x)) # And max of y or x is the movement
	
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
		
	if j.get_button(0): # Left
		if DServo0Cur < DServo0[1]:
			DServo0Cur = DServo0Cur + 100
			
	if j.get_button(2): # Right
		if DServo0Cur > DServo0[0]:
			DServo0Cur = DServo0Cur - 100
			
	if j.get_button(1): # Down
		if DServo1Cur < DServo1[1]:
			DServo1Cur = DServo1Cur + 100

	if j.get_button(3): # Up
		if DServo1Cur > DServo1[0]:
			DServo1Cur = DServo1Cur - 100

	if j.get_button(9): # Start. Reset to Default positions
		DServo0Cur = DServo0[2]
		DServo1Cur = DServo1[2]

	# Poll Joystick for X/Y cordinates
	x = j.get_axis(2) # Left/Right
	y = j.get_axis(1) # Forward/Reverse

	left, l_drive, right, r_drive = tankdrive(x,y) # Call tankdrive()

	print(left,l_drive,right,r_drive)
	try:
		bus.write_i2c_block_data(device, 1, [r_drive, l_drive, right, left, DServo0Cur/10, DServo1Cur/10])
	except IOError, err:
		print "Lost I2C"
		
	time.sleep(0.1) # Sleep 100ms
