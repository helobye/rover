import smbus
import time

# RPi rev 1 = SMBus(0)
# RPi rev 2 = SMBus(1)
bus = smbus.SMBus(1)

device = 0x04

def writeNumber(value):
	bus.write_byte(device, value)
	# bus.write_byte_data(address, 0, value)
	return -1

def getStatus(device):
		status = ""
		for i in range (0, 5):
			#temp = bus.read_byte(device)
			#print temp, chr(temp)
			status += chr(bus.read_byte(device))
			time.sleep(0.05);
		time.sleep(0.1)        
		return status
		
		
while True:
	#ret_status = getStatus(device)
	#print ret_status , ret_status.encode("hex")
	snd_arr = bytearray()
	snd_arr.append(0x01)
	snd_arr.append(0x02)
	snd_arr.append(0x02)
	snd_arr.append(0x64)
	snd_arr.append(0x64)
	bus.write_i2c_block_data(device,1,[0, 0, 150,150])
	#print StringToBytes("test")
	#writeNumber(1)
	#writeNumber(2)
	#writeNumber(2)
	#writeNumber(150)
	#writeNumber(150)
	ret_arr = bytearray()
	ret_arr.append(0x30)
	ret_arr.append(0x31)
	ret_arr.append(0x32)
	ret_arr.append(0x33)
	ret_arr.append(0x34)
	#asdf = bus.read_byte_data(device,0)
	ret_arr = bus.read_i2c_block_data(device,5)
	print ret_arr[0], ret_arr[1], ret_arr[2]*4, ret_arr[3]*4, ret_arr[4]*4
	del ret_arr
	time.sleep(0.1)
