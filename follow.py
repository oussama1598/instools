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
assert api.searchUsername(instaUsername)

userId = api.LastJson['user']['pk']

assert api.getUserFeed(userId)

posts = api.LastJson['items']

postByCode = [post for post in posts if post['code'] == instaPostId][0]
postId = postByCode['pk']

assert api.getMediaLikers(postId)

likers = api.LastJson['users']

print('Found {} likers'.format(len(likers)))

while count <= len(likers) and count < maxPerDay:
	print('{}: Following the Sequence {}'.format(datetime.now(), count // maxPerHour))
	print('{} left'.format(len(likers)))

	i = 0
	while True:
		liker = likers[randint(0, len(likers) - 1)]

		assert api.userFriendship(liker['pk'])

		followed = api.LastJson['following']
		requested = api.LastJson['outgoing_request']

		if not followed and not requested:
			try:
				assert api.follow(liker['pk'])

				print('{} Followed {}'.format(count + 1, liker['username']))
				count += 1
				i += 1
			except:
				print('Can\'t Follow This person {}'.format(liker['username']))
		else:
			print('Already followed {}'.format(liker['username']))

		likers.remove(liker)

		if i >= maxPerHour:
			break

	print('Done with the sequence number {}'.format(count // maxPerHour))
	print('{}: Delaying for 60 minutes'.format(datetime.now()))
	print('Next sequence in {}'.format(datetime.now() + timedelta(minutes = 60)))
	time.sleep(60 * 60)