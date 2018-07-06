#!/usr/bin/env python
from __future__ import division
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from mopidy_json_client import MopidyClient
from mopidy_json_client.formatting import print_nice
import random
import zmq
#from threading import Thread
#import threading
#from threading import Thread
import threading
#status = "music"
status = "time"
tr = ""
mopid = ""
disco = False
li = 20
loc = 5
maxlen = 10

def getlen():
    time.sleep(5)
    global loc
    global maxlen
    while True:
        tl_track = mopid.playback.get_current_tl_track(timeout=15)
        loc = mopid.playback.get_time_position()
     #   print(mopid.playback.get_time_position())
        maxlen = tl_track.get('track').get('length')

        time.sleep(0.3)

def getstate():
    time.sleep(5)
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5556")
    while True:
        message = socket.recv()
        print("Received request: %s" % message)
        socket.send(b"Ack")
        global status
        status = message
        

s = threading.Thread(target=getlen)
t = threading.Thread(target=getstate)
s.daemon = True
t.daemon = True
def playback_state_changed(old_state, new_state):
  #  self.state = new_state
    #print_nice('> Playback state changed to ', new_state + old_state)
    if new_state == "paused":
        global tr
        tr = ""
    else:
        global tr
        tr = "loading"
        tl_track = mopid.playback.get_current_tl_track(timeout=15)
        track = tl_track.get('track') if tl_track else None
        name = track.get('name')
        artists = ', '.join([artist.get('name') for artist in track.get('artists')])
        tr = "" + artists + " - " + name

def updatetrack(tl_track):
    track = tl_track.get('track') if tl_track else None
    if not track:
        tr = ''
        return
    global tr
    name = track.get('name')
    artists = ', '.join([artist.get('name') for artist in track.get('artists')])
    tr = "" + artists + " - " + name

    print("track updated to: " + tr)
class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")
        super(RunText, self).__init__()

        print('Starting Mopidy to Matrix')

        # Init variables
        self.state = 'stopped'
        self.uri = None
        self.save_results = False
        self.debug_flag = False

        # Instantiate Mopidy Client
        self.mopidy = MopidyClient(
            ws_url='ws://192.168.178.220:6680/mopidy/ws',
            autoconnect=False,
            retry_max=10,
            retry_secs=10
        )
        self.mopidy.bind_event('track_playback_started', updatetrack)
        self.mopidy.bind_event('playback_state_changed', playback_state_changed)
        self.mopidy.debug_client(self.debug_flag)
        self.mopidy.connect()
        global mopid
        mopid = self.mopidy
        
        s.start()
        t.start()
      #  time.sleep(1.55)
      ##  state = self.mopidy.playback.get_state(timeout=5)
      #  if state == "Playing":
     #       self.mopidy.playback.pause()
   #         self.mopidy.playback.resume()

     #  tl_track = mopid.playback.get_current_tl_track(timeout=15)
     #  track = tl_track.get('track') if tl_track else None
     #  if track != None:
     #      name = track.get('name')
     #      artists = ', '.join([artist.get('name') for artist in track.get('artists')])
     #      tr = "" + artists + " - " + name
     #  else:
     #      tr = ""

        #    trackinfo = {
         #       'name': track.get('name'),
        #        'artists': ', '.join([artist.get('name') for artist in track.get('artists')])
   #         }
          # tr = track.get('name')
           # print('Now playing: {artists} - {name}'.format(**trackinfo))

    def track_playback_started(self, tl_track):
        track = tl_track.get('track') if tl_track else None
        self.uri = track.get('uri') if track else None
        print_nice('> Current Track: ', track, format='track')

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x13.bdf")
      #  r = random.randint(1, 255)
      #  g = random.randint(1, 255)
      #  b = random.randint(1, 255)
      #  textColor = graphics.Color(r, g, b)
        pos = offscreen_canvas.width
       # my_text = self.args.text

        while True:
            offscreen_canvas.Clear()
            global disco
            if disco == True:
                r = random.randint(1, 255)
                g = random.randint(1, 255)
                b = random.randint(1, 255)
            else:
                r = 255
                g = 255
                b = 0 

            textColor = graphics.Color(r, g, b)
            global li
            global status
           # print(status)


            if status == "music":
                global loc
                global maxlen
                

                breed = loc / maxlen * 32
                len = graphics.DrawText(offscreen_canvas, font, pos, 12, textColor, tr)
                if tr != "":
                    lenr = graphics.DrawLine(offscreen_canvas, 0, 15, breed, 15, textColor)
                pos -= 1
                if (pos + len < 0):
                    pos = offscreen_canvas.width
    
                time.sleep(0.05)
                
            elif status == "time":
                localtime   = time.localtime()
                timeString  = time.strftime("%H:%M", localtime)
                minu  = time.strftime("%M", localtime)
                if int(minu) % 5 == 0:
                    x = 0
                    y = 14
                elif int(minu) % 3 == 0:
                    x = 3
                    y = 12
                else:
                    x = 1
                    y = 15
               # print(timeString)
                leni = graphics.DrawText(offscreen_canvas, font, x, y, textColor, timeString)
            else:
                pass
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
#sudo python music.py --led-no-hardware-pulse true -r 16 --led-cols 32
# Main function
if __name__ == "__main__":
   # super(RunText, self).__init__()
  #  demo = RunText(debug=False)
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
