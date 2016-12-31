import requests
import json

def send_message(data, channel="#fantasy-first", icon=":robot_face:", name="Fantasy FIRST Bot"):
	f = open("data/slackurl.txt")
	payload = {"channel": channel, "username": name,"text": data, "icon_emoji": icon}
	results = requests.post(f.readline(), json.dumps(payload), headers={'content-type': 'application/json'})

	f.close()
	return results.text