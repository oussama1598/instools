#!/usr/bin/env python

from InstagramAPI import InstagramAPI
from datetime import datetime, timedelta
from random import randint
import time
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--username", required=True,
	help="insta's username")
ap.add_argument("-p", "--password", required=True,
	help="insta's password")
ap.add_argument("-m", "--message", required=True,
	help="The message to be sent")
args = vars(ap.parse_args())

username, password = args['username'], args['password']
message = args['message']


api = InstagramAPI(username, password)

assert api.login()
assert api.SendRequest('friendships/pending?')

users = api.LastJson['users']

while True:
    for user in users:
        userId = user['pk']
        userName = user['username']
        
        # approve follow request	
        assert api.approve(userId)
        print('User {} approved {}'.format(userName, datetime.now())) 
        
        # send Message to the user
        assert api.direct_message(message, userId)
        print('Sent messsage to {}'.format(userName)) 


    print('{} Sleeping for 20 minutes'.format(datetime.now()))
    time.sleep(60 * 20)
