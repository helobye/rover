import pygame
import time
import smbus

# RPi rev 1 = SMBus(0)
# RPi rev 2 = SMBus(1)
bus = smbus.SMBus(1)

device = 0x04

# Servos. Min, Max, Default
DServo0 = [700,2200,1500] # DServo0 L/R: Left:700, Right: 2200 Center:1500 
DServo1 = [700,2300,2300] # DServo1 TIlt: Backard: 700, Forward: 2300, Max: 2300

def limit(n):
	if n > 1:
		return 1
	elif n < -1:
		return -1
	else:
		return n


pygame.init()
j = pygame.joystick.Joystick(0)
j.init()
 
print 'Initialized Joystick : %s' % j.get_name()
		
pygame.event.pump()

if j.get_button(0): # Left
	if DServo0 < DServo0[1]:
		DServo0 = DServo0 + 100
		print DServo0
if j.get_button(2): # Right
	if DServo0 > DServo0[0]:
		DServo0 = DServo0 - 100
		print DServo0
if j.get_button(1): # Down
	if DServo1 < DServo1[1]:
		DServo1 = DServo1 + 100
		print DServo1
if j.get_button(3): # Up
	if DServo1 > DServo1[0]:
		DServo1 = DServo1 - 100
		print DServo1
if j.get_button(9): # Start. Reset to Default positions
	DServo0 = DServo0[2]
	DServo1 = DServo1[2]

x = j.get_axis(0)
y = j.get_axis(1)
z = j.get_axis(2)

left  = y - z
right = y + z
        
maxi = max(left, right)
        
if maxi > 1:
	left = left/maxi
	right = right/maxi
    
left = limit(left)
right = limit(right)
	
move_y = int(round(left * 250, 0))
if (move_y < 0):
	drive_y = 2
#elif (move_y == 0):
#	drive_y = 1
else:
	drive_y = 0
pwm_y = abs(move_y)

move_z = int(round(right * 250, 0))
if (move_z < 0):
	drive_z = 2
#elif (move_z == 0):
#	drive_z = 1
else:
	drive_z = 0
pwm_z = abs(move_z)
	
print(pwm_y,drive_y,pwm_z,drive_z)
try:
	bus.write_i2c_block_data(device,1,[drive_y, drive_z, pwm_y,pwm_z,DServo0/10,DServo1/10])
except IOError, err:
	print "Lost I2C"
time.sleep(0.1)
