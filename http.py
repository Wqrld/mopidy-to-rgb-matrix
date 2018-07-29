# -*- coding: utf-8 -*-

import requests
import json
import pprint
from phue import Bridge
import datetime
b = Bridge('192.168.178.12')
#b.connect()
lights = b.lights

# Print light names
if b.get_light(1, 'on'):
  licht = 'aan'
else:
  licht = 'uit'

print licht
#print new date()
rw = requests.get('https://api.wunderground.com/api/e716c35379e664c4/conditions/q/pws:IDENHAAG87.json')
jw = rw.json()

iw = str(jw['current_observation']['temp_c'])
#iw = str(jw['version'])
print 'Het is buiten ' + iw + ' graden.'
#(while true; do python klok.py; sleep 1200; done;) | sudo ./text-example -f ../fonts/6x13.bdf -b 30 -x 2 --led-rows=16 --led-no-hardware-pulse -y 1 --led-pwm-lsb-nanoseconds=600 --led-scan-mode=0


url = "http://raspberry.local:6680/mopidy/rpc"
headers = {'content-type': 'application/json'}

    # Example echo method
payload = {
    "method": "core.playback.get_state",
    "params": {},
    "jsonrpc": "2.0",
    "id": 1,
}
response2 = requests.post(url, data=json.dumps(payload), headers=headers).json()
print str(response2["result"])
ry = requests.get('https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UCyXLE_LjnjK7QBFDYLBnImQ&key=AIzaSyAuAEhVtPPAz4ahIVacEU0RfDYDCu_pO2U')
jy = ry.json()

print 'Ik heb ' + jy['items'][0]['statistics']['subscriberCount'] + ' subs.'



tr = requests.get('https://api.twitch.tv/kraken/streams/lucgameztwitch?oauth_token=yyejrtrybldt3egoo8lpx4i0z0lbju')
tj = tr.json()

#curl https://api.twitch.tv/kraken/streams/lucgameztwitch?oauth_token=yyejrtrybldt3egoo8lpx4i0z0lbju
if tj["stream"] is None:
  print 'De stream is offline.'
  stre = "niet"
else:
  print 'De stream is live.'
  stre = "live"

#{
#"access_token": "yyejrtrybldt3egoo8lpx4i0z0lbju",
#"refresh_token": "bb094bfnoul8u0ycc1naokke68hoieye7ayizk3889wep15v8l",
#"scope": [
#"channel_feed_read"
#]
#}
headers = {'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAKz9zgAAAAAA%2Fgu8jog2YlxDqbtiAq2E5igZBKM%3DrNewGrVKMLofuCKpB5YlWDMvGerL2DzJ8rGJJrABr26WZ3TwyC'}
rt = requests.get('https://api.twitter.com/1.1/users/show.json?screen_name=wereld03', headers=headers)
jt = rt.json()
#print str(jt['followers_count'])
print 'Ik heb ' + str(jt['followers_count']) + ' followers.'
#M0JBOVk2cjdLb0wzWGtRbXRqOHQwMGd5TDpSTG5VN0Y5SFFyTzZQclZySDF4MW1CMUt0S2xLNkE1cWtZUDA4Q0JiOTVhQm9UbHEwcg==
#data = json.loads(rt.text)

file = open("txt","w")

file.write(iw + "\n")
file.write(jy['items'][0]['statistics']['subscriberCount'] + "\n")
file.write(stre + "\n")
file.write(response2["result"] + "\n")
file.write(licht + '\n')
file.write(str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute) + "\n")
file.write(str(jt['followers_count']) + "\n")
#file.write("cmon")

file.close()
print 'done'
#for itemt in jy:
#  st = itemt.get("followers_count")
#print 'ik heb ' + st + ' subs'


#ip = str(data['followers_count'])
#c#ount
#print jt.get([followers_count])
#ParsedValue = data['followers_count']
#pprint(data["followers_count"][0])
#print test
#print ip
#for itemt in jt:
 # st = itemt.get("followers_count")
#print 'ik heb ' + st + ' subs'
#it = str(jt['followers_count'])
#print 'ik heb ' + it + ' followers'

