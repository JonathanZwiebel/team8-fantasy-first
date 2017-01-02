import requests
import json

def send_message(data, attach="", channel="#fantasy-first-bot", icon=":robot_face:", name="Fantasy FIRST Bot"):
	f = open("data/slackurl.txt")
	payload = {"channel": channel, "username": name,"text": data, "icon_emoji": icon, "attachments": attach}
	results = requests.post(f.readline(), json.dumps(payload), headers={'content-type': 'application/json'}, timeout=1)

	f.close()
	return results.text