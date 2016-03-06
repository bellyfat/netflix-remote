#!/usr/bin/python

touchmouse_port = 4026

import socket

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind(("", touchmouse_port))
tcp_socket.listen(1)

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(("", touchmouse_port))
print "Waiting ..."
while 1:
    data, addr = udp_socket.recvfrom(8)
    data = map(ord, data) # bytes->integer codes
    print data
    if data[3] == 13: # keyboard code
        print data[7]
        
