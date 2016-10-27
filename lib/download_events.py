import requests
import os
from collections import Counter
import json

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

key =  os.environ['MEETUP_API_KEY']
lat = "29.761993"
lon = "-95.366302"

with open('data/groups.json') as group_file:
    groups_json = json.load(group_file)

groups = [str(group['id']) for group in groups_json]
for idx, chunk in enumerate(chunks(groups, 200)):
    print idx, chunk
    results = []
    group = ",".join(chunk)
    uri = "https://api.meetup.com/2/events?&group_id={0}&lat={1}&lon={2}&key={3}&fields=announced_at&status=upcoming,past".format(group, lat, lon, key)

    while True:
        if uri is None:
            break
        response = requests.get(uri).json()
        for result in response["results"]:
            results.append(result)
        uri = response["meta"]["next"] if response["meta"]["next"] else None
    with(open("data/events/{0}.json".format(idx), 'w')) as events_file:
        json.dump(results, events_file)
