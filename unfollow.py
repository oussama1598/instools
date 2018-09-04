#!/usr/bin/env python

from InstagramAPI import InstagramAPI
from datetime import datetime, timedelta
from random import randint
import time
import sys
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--username", required=True,
	help="insta's username")
ap.add_argument("-p", "--password", required=True,
	help="insta's password")
ap.add_argument("-w", "--followwho", required=True,
	help="The username to follow from")
ap.add_argument("-ps", "--posttofollow", required=True,
	help="The post to follow likers from")
ap.add_argument("-mh", "--maxperhour", default=160,
	help="Max per hour", type=int)
ap.add_argument("-md", "--maxperday", default=600,
	help="Max per day", type=int)
args = vars(ap.parse_args())


username, password = args['username'], args['password']
instaUsername, instaPostId = args['followwho'], args['posttofollow']
maxPerHour, maxPerDay = args['maxperhour'], args['maxperday']
count = 0

api = InstagramAPI(username, password)

assert api.login()
assert api.getSelfUsersFollowing()

users = api.LastJson['users']

print('Found {} users'.format(len(users)))

while count <= len(users) and count < maxPerDay:
	print('{}: Unfollowing the Sequence {}'.format(datetime.now(), count // maxPerHour))

	i = 0
	while True:
		user = users[randint(0, len(users) - 1)]

		try:
			assert api.unfollow(user['pk'])

			print('{} Unfollowed {}'.format(count + 1, user['username']))
			count += 1
			i += 1
		except:
			print('Can\'t unfollow This person {}'.format(user['username']))

		users.remove(user)

		if i >= maxPerHour:
			break

	print('Done with the sequence number {}'.format(count // maxPerHour))
	print('{}: Delaying for 60 minutes'.format(datetime.now()))
	print('Next sequence in {}'.format(datetime.now() + timedelta(minutes = 60)))
	time.sleep(60 * 60)