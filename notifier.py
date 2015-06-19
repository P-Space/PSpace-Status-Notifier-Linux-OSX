import argparse
import urllib2
import json
from subprocess import call
import os
import threading
import time

#home = getenv("HOME")
folder = os.path.dirname(os.path.realpath(__file__))
oldstatus=-1
olddate=0

def DisplayMessage(title, message):
	global home
	call(['notify-send', title, message,'-t','3000','-i',folder+'/icon.png'])
	#call['notify-send', title+' '+message+', '+displ_time+' --hint=int:transient:1  -i ~/.pspace-notifier/pspace.png']

def EventCheck():
	global olddate
	try:
		url = urllib2.urlopen('http://pspace.dyndns.org:49004/report/?json&limit=1')
		if url.getcode() != 200:
			print 'problem occured. http status:', url.getcode()
		else:
			event = json.loads(url.read())
			newdate = int(event['events'][0]['t'])
			if(olddate!=newdate):
				DisplayMessage('P-Space door event',event['events'][0]['extra'])
				olddate=newdate
	except URLError:
		olddate=0

def StatusCheck():
	global oldstatus
	try:
		url = urllib2.urlopen('http://www.p-space.gr/status')
		if url.getcode() != 200:
			print 'problem occured. http status:', url.getcode()
		else:
			newstatus = int(url.read())
			if(oldstatus!=newstatus):
				if(newstatus==1):
					status='open'
				else:
					status='closed'
				oldstatus=newstatus
				DisplayMessage('P-Space status changed','P-Space is now '+status)
	except URLError:
		oldstatus=-1

def SetOpen(set):
	try:
		url = urllib2.urlopen('http://www.p-space.gr/status/set.php?'+set)
		if url.getcode() != 200:
			print 'problem occured. http status:', r1.status, r1.reason
	except URLError:
		print 'URL exception occured.'

def tick():
	EventCheck()
	StatusCheck()


parser = argparse.ArgumentParser(description='P-Space Status and Event Notifier for Linux - eparon 2014 v0.1')
parser.add_argument('-t','--time', help='Specify the refresh interval in seconds',type=int)
parser.add_argument('-r','--run', help='Set this flag in order to run in the background. Otherwise will only check once for status and last event.', action='store_true')
parser.add_argument('-s','--set',help='Set status - Use type \'open\' or \'close\'', choices=['open','close'])

args = parser.parse_args()

if args.set:
	SetOpen(args.set)

if args.run:
	if args.time:
		ts=args.time
	else:
		ts=1.0
	while 1==1:
		tick()
		time.sleep(ts)
else:
	tick()

