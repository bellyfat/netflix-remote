#!/usr/bin/python

touchmouse_port = 4026

import socket

# The app looks for an open listening TCP socket on port 4026
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SO_REUSEADDR lets me run this code over and over without getting
# "Address already in use"
tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_socket.bind(("", touchmouse_port))
tcp_socket.listen(1)

# The actual data comes in on UDP on the same port
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(("", touchmouse_port))
print "Waiting ..."
while 1:
    data, addr = udp_socket.recvfrom(8)
    data = map(ord, data) # bytes->integer codes

    if data[3] == 13: # keyboard code
        print chr(data[7])
        
