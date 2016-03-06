#!/usr/bin/python

class SpacebarDevice(object):
    def __init__(self):
        self._device = uinput.Device([uinput.KEY_SPACE])
    def send_pause(self):
        self._device.emit_click(uinput.KEY_SPACE)

touchmouse_port = 4026

# to install uinput:
# apt-get install libudev-dev
# pip install python-uinput

import socket, uinput

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

spacebar = SpacebarDevice()
while 1:
    data, addr = udp_socket.recvfrom(8)
    data = map(ord, data) # bytes->integer codes

    if data[3] == 13: # keyboard code
        if 'a' < chr(data[7]) < 'z':
            spacebar.send_pause()
        
