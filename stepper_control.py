#!/usr/bin/python37all

from stepper import Stepper 
from stepper import moveSteps
from stepper import halfstep
import cgi
import json
from urllib.request import urlopen
from urllib.parse import urlencode

data = cgi.FieldStorage()
s1 = data.getvalue('slider1') #gets slider value from website
act = data.getvalue('action') #gets led value from website

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('</head>')
print('<body>')
print('<div style="width:600px;background:#40E0D0;border:1px;text-align:center">')
print('<br>')
print('<font size="3" color="black" face="helvetica">')
print('<b>Lab 5 Stepper</b>')
print('<br><br>')

slide = {"slider1":s1, "action":act} #creates slide dictionary for slider and Led variables
with open('s.txt', 'w') as f: 
  json.dump(slide,f) #uses json to dump dictionary into file

print('<html>')
print('<form action="/cgi-bin/stepper_control.py" method="POST">')
print('<input type="range" name="slider1" min="0" max="360" value="%s"><br>' % s1)
print('<input type="submit" name="action" value="rotate" />')
print('<input type="submit" name="action" value="zero" />')
print('</form>')
print('Angle = %s' % s1)
print('act = ', act)
print('<iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1552343/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&xaxis=Motor+Angle&yaxis=Motor+Angle"></iframe>')
print('<iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1552343/widgets/375143"></iframe>')
print('</html>')

