#!/usr/bin/python

class NetflixDevice(object):
    def __init__(self):
        self._device = uinput.Device([uinput.KEY_SPACE,
                                      uinput.KEY_LEFT,
                                      uinput.KEY_RIGHT,
                                      uinput.KEY_LEFTSHIFT])
    def toggle_pause(self):
        self._device.emit_click(uinput.KEY_SPACE)

    def rewind(self):
        self._device.emit_combo([uinput.KEY_LEFTSHIFT,
                                 uinput.KEY_LEFT])

    def fast_forward(self):
        self._device.emit_combo([uinput.KEY_LEFTSHIFT,
                                 uinput.KEY_RIGHT])
        

touchmouse_port = 4026

# to install uinput:
# apt-get install libudev-dev
# pip install python-uinput

import socket, uinput

def publish_service(port):
    import os
    if os.fork() == 0:
        os.execl("/usr/bin/avahi-publish", "avahi-publish",
                 "-s", socket.gethostname(),
                 "_iTouch._tcp", str(port))
publish_service(touchmouse_port)

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

netflix = NetflixDevice()
while 1:
    data, addr = udp_socket.recvfrom(8)
    data = map(ord, data) # bytes->integer codes

    if data[3] == 13: # keyboard code
        qq = chr(data[7])
        if  qq in "qwaszxedc":
            netflix.rewind()
        elif qq in "rfvtgbyhn":
            netflix.toggle_pause()
        elif qq in "ujmikolp":
            netflix.fast_forward()
