# netflix-remote

Use your iPhone to control Netflix running on your Linux machine. 

### How it works

A simple Python server runs on your Linux machine and listens for UDP
commands from your iPhone. It generates keyboard input events
corresponding to Netflix keyboard shortcuts.

The implementation is tiny. You can adapt it for own
remote-controlling needs.

I wrote a [blog
post](http://kshitijl.github.io/intro/2016/02/18/remote/) about how I
made this work.

### Installation

On your Linux machine:

    sudo apt-get install libudev-dev
    sudo pip install python-uinput

Install the TouchMouse app from Logitech on your iPhone.

Clone this repository.

### Start the server

You need `sudo` permissions to send input events to `/dev/uinput`.

1. Run `./launch-server` from this repo.
1. Start playing something on Netflix and give that window focus.
1. Open the app and select your Linux machine by its `hostname`.

### Use the app

On the TouchMouse app, bring up the keyboard.

* Tap on the left side of the keyboard to rewind a little.
* Tap in the middle to pause.
* Tap on the right side to fast-forward.
* Press space to toggle fullscreen.
* Press any number `0-9` to close the browser tab.

### Launch Netflix from your laptop

To start Netflix over `ssh` on the main monitor:

    DISPLAY=:0 google-chrome <netflix video url>

### Credits

* [Logitech TouchMouse app](https://itunes.apple.com/us/app/touch-mouse/id338237450?mt=8)
* https://github.com/mycroes/touchmoused for some details of the Logitech TouchMouse protocol
* https://github.com/tuomasjjrasanen/python-uinput for Python bindings to Linux `uinput`

### License

MIT