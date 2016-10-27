import requests
import os
from collections import Counter
import json

key =  os.environ['MEETUP_API_KEY']
lat = "29.761993"
lon = "-95.366302"

with open('data/groups.json') as group_file:
    groups_json = json.load(group_file)

groups = [str(group['id']) for group in groups_json]

for group in groups:
    print group
    members_file = "data/members/{0}.json".format(group)
    if os.path.isfile(members_file):
        print "Members {0}: Already processed [{1}]".format(group, os.stat(members_file).st_size)
        continue
    else:
        print "Members {0}: Processing".format(group)

    print "processing group {0}".format(group)
    results = []
    uri = "https://api.meetup.com/2/members?&group_id={0}&lat={1}&lon={2}&key={3}".format(str(group),lat,lon, key)
    while True:
        if uri is None:
            break
        r = requests.get(uri)

        headers = r.headers
        remaining = headers["X-RateLimit-Remaining"]
        reset = headers["X-RateLimit-Reset"]

        print "-> remaining: {0}, reset: {1}".format(remaining, reset)

        response = r.json()
        #print response
        for result in response["results"]:
            results.append(result)
        uri = response["meta"]["next"] if response["meta"]["next"] else None
    with(open(members_file, 'w')) as members_file:
        json.dump(results, members_file)
