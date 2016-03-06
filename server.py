#!/usr/bin/python

# to install uinput:
# apt-get install libudev-dev
# pip install python-uinput
import uinput        
class NetflixDevice(object):    
    def __init__(self):
        self._device = uinput.Device([uinput.KEY_SPACE,
                                      uinput.KEY_F,
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

    def fullscreen(self):
        self._device.emit_click(uinput.KEY_F)
        
import socket
class TouchmouseServer(object):
    touchmouse_port = 4026
    def __init__(self):
        self.listen_tcp()
        self.publish_service()
        self.listen_udp()
        
    def publish_service(self):
        import os
        if os.fork() == 0:
            os.execl("/usr/bin/avahi-publish", "avahi-publish",
                     "-s", socket.gethostname(),
                     "_iTouch._tcp", str(self.touchmouse_port))

    def listen_tcp(self):
        # The app looks for an open listening TCP socket on port 4026
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # SO_REUSEADDR lets me run this code over and over without getting
        # "Address already in use"
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_socket.bind(("", self.touchmouse_port))
        tcp_socket.listen(1)

        self.tcp_socket = tcp_socket # make a reference to prevent it being garbage-collected

    def listen_udp(self):
        # The actual data comes in on UDP on the same port
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind(("", self.touchmouse_port))


    def event_loop(self, handler):
        while 1:
            data, addr = self.udp_socket.recvfrom(8)
            data = map(ord, data) # bytes->integer codes
            handler(data)
    
if __name__ == "__main__":
    netflix = NetflixDevice()
    def netflix_handler(iphone_input):
        data = iphone_input
        if data[3] == 13: # keyboard code
            qq = chr(data[7])
            if  qq in "qwaszxedc":
                netflix.rewind()
            elif qq in "rfvtgbyhn":
                netflix.toggle_pause()
            elif qq in "ujmikolp":
                netflix.fast_forward()
            elif qq in " ":
                netflix.fullscreen()

    server = TouchmouseServer()
    server.event_loop(netflix_handler)
