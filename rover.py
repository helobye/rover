import pygame	# Used for Joystick
import time	# Used for Sleep
import smbus	# Used for i2c

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

def limit(n):
	if n > 1:
		return 1
	elif n < -1:
		return -1
	else:
		return n

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

	# Poll Joystick for XYZ cordinates
	x = j.get_axis(0)
	y = j.get_axis(1)
	z = j.get_axis(2)

	# Define Tank Style controls
	left  = y - z
	right = y + z
        
        # Make sure left, right values do not exceed maximum
	maxi = max(left, right)
        
	if maxi > 1:
		left = left/maxi
		right = right/maxi
    
	left = limit(left)
	right = limit(right)
	
	# Y axis (Forward/Reverse)
	move_y = int(round(left * 250, 0))
	if (move_y < 0):
		drive_y = 2
	else:
		drive_y = 0
	pwm_y = abs(move_y)

	# Z Axis (Left/Right)
	move_z = int(round(right * 250, 0))
	if (move_z < 0):
		drive_z = 2
	else:
		drive_z = 0
	pwm_z = abs(move_z)
	
	print(pwm_y,drive_y,pwm_z,drive_z)
	try:
		bus.write_i2c_block_data(device,1,[drive_y, drive_z, pwm_y,pwm_z,DServo0Cur/10,DServo1Cur/10])
	except IOError, err:
		print "Lost I2C"
		
	# Sleep 100ms
	time.sleep(0.1)
