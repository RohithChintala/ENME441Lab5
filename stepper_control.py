#!/usr/bin/python37all
from stepper import Stepper 
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
with open('StepperSteps.txt', 'w') as f: 
  json.dump(slide,f) #uses json to dump dictionary into file

print('<html>')
print('<form action="/cgi-bin/stepper_control.py" method="POST">')
print('<select name="menu_choice">')
print('<option name="option" value="a"> Rotate Stepper</option>')
print('<option name="option" value="b"> Zero Stepper</option>')
print('</select>')
print('<input type="range" name="slider1" min="0" max="360" value="%s"><br>' % s1)
print('<input type="submit" name="action" value="rotate" />')
print('<input type="submit" name="action" value="zero" />')
print('</form>')
print('Angle = %s' % s1)
print('<iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1552343/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&xaxis=Motor+Angle&yaxis=Motor+Angle"></iframe>')
print('<iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1552343/widgets/373407"></iframe>')
print('</html>')


'''
api = "QYSPJIYIF0S3QIEU"   #####CORRECT FOR MY API


params = {
  "api_key":api,
  1: s1}
params = urlencode(params)   # put dict data into a GET string

  # add "?" to URL and append with parameters in GET string:
url = "https://api.thingspeak.com/update?" + params
try:
  response = urlopen(url)      # open the URL to send the request
  print(response.status, response.reason)  # display the response
  print(response.read()) # display response page data
  time.sleep(16)    # 15 sec minimum
except Exception as e:
  print(e)
'''