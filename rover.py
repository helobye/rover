import smbus  # Used for i2c
import socket # Used for client communications
#import sys
#import select

address = ('192.168.1.10', 6005)
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(address)

bus = smbus.SMBus(1) # RPi rev 2 = SMBus(1)
device = 0x04 # Arduino i2c device address

while True:
        print "Listening"
        recv_data, addr = server_socket.recvfrom(2048)
        #if recv_data == "Request 1" :
        #       print "Received request 1"
        #       server_socket.sendto("Response 1", addr)
        #elif recv_data == "Request 2" :
        #       print "Received request 2"
        #       data = "Response 2"
        #       server_socket.sendto(data, addr)
        recv_data = recv_data.strip('[]').split(',')
        recv_data = [int(x) for x in recv_data]
        r_drive = recv_data[0]
        l_drive = recv_data[1]
        right = recv_data[2]
        left = recv_data[3]
        DServo0Cur = recv_data[4]
        DServo1Cur = recv_data[5]

        print r_drive, l_drive, right, left, DServo0Cur, DServo1Cur
        try:
                bus.write_i2c_block_data(device, 1, [r_drive, l_drive, right, l$
        except IOError, err:
                print "Lost I2C"
