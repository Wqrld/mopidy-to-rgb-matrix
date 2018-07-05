#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from mopidy_json_client import MopidyClient
from mopidy_json_client.formatting import print_nice
import random
tr = ""
mopid = ""
disco = False
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
        font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/7x13.bdf")
      #  r = random.randint(1, 255)
      #  g = random.randint(1, 255)
      #  b = random.randint(1, 255)
      #  textColor = graphics.Color(r, g, b)
        pos = offscreen_canvas.width
       # my_text = self.args.text

        while True:
            offscreen_canvas.Clear()
          #  tl_track = self.mopidy.playback.get_current_tl_track(timeout=15)
          #  self.track_playback_started(tl_track)

          #  track = tl_track.get('track') if tl_track else None
          #  self.uri = track.get('uri') if track else None
          #  tr = track['name']



          #  print(track['name'])
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
            len = graphics.DrawText(offscreen_canvas, font, pos, 15, textColor, tr)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

#sudo python music.py --led-no-hardware-pulse true -r 16 --led-cols 32
# Main function
if __name__ == "__main__":
   # super(RunText, self).__init__()
  #  demo = RunText(debug=False)
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
