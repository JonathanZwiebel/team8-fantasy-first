import urllib2
import json

def get_matches_with_teams(eventKey):
	"""
	Method that will return a list of TBAMatch
	"""
	url = "http://www.thebluealliance.com/api/v2/event/" + eventKey + "/matches" + '?X-TBA-App-Id=frc8%3Ascouting%3Apre-alpha'
	request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'})
	data = urllib2.urlopen(request).read().decode('utf-8')
	jsonvar = json.loads(data)

	return_val = []
	for i in jsonvar:
		return_val.append(BasicTBAMatch(i))

	return return_val


def get_match(matchkey):
	"""
	Method that will return a SuperMatch

	Note that the matchKey can be obtained using the key from the BasicTBAMatch object
	"""
	url = "http://www.thebluealliance.com/api/v2/match/" + matchkey + '?X-TBA-App-Id=frc8%3Ascouting%3Apre-alpha'
	request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'})
	data = urllib2.urlopen(request).read().decode('utf-8')
	jsonvar = json.loads(data)

	return FullTBAMatch(jsonvar)


class Alliance:
	def __init__(self, team1, team2, team3):
		self.teams = [team1, team2, team3]
		self.teams = [a.encode('ascii','ignore') for a in self.teams]

	def get_teams(self):
		return self.teams

	def as_string(self):
		return " ".join(self.teams)

class BasicTBAMatch(object):

	def __init__(self, match_dict):
		self.comp_level = match_dict["comp_level"]
		self.match_number = match_dict["match_number"]
		self.key = match_dict["key"].encode('ascii', 'ignore')

		self.blue_alliance = Alliance(match_dict["alliances"]["blue"]["teams"][0],
									  match_dict["alliances"]["blue"]["teams"][1],
									  match_dict["alliances"]["blue"]["teams"][2])
		self.red_alliance = Alliance(match_dict["alliances"]["red"]["teams"][0],
									  match_dict["alliances"]["red"]["teams"][1],
									  match_dict["alliances"]["red"]["teams"][2])

	def get_key(self):
		return self.key

	def get_key_as_displayable(self):
		display = self.key.split("_")[1]

		if display[0:2] == "qm":
			return display.split("qm")[1]
		else:
			return display

	def get_red_alliance(self):
		return self.red_alliance

	def get_blue_alliance(self):
		return self.blue_alliance

class FullTBAMatch(object):

	"""
	Treat the "performance" instance variables as a dictionary with the 
	following keys

	  "teleopPoints"
      "robot3Auto"
      "breachPoints"
      "autoPoints"
      "teleopScalePoints"
      "autoBouldersLow"
      "teleopTowerCaptured"
      "teleopBouldersLow"
      "teleopCrossingPoints"
      "foulCount":
      "foulPoints"
      "towerFaceB"
      "towerFaceC"
      "towerFaceA"
      "techFoulCount"
      "totalPoints"
      "adjustPoints"
      "position3"
      "robot1Auto"
      "position4"
      "position5"
      "autoBoulderPoints"
      "teleopBoulderPoints"
      "teleopBouldersHigh"
      "autoBouldersHigh"
      "robot2Auto"
      "position1crossings"
      "towerEndStrength"
      "position4crossings"
      "position2crossings"
      "position5crossings"
      "position3crossings"
      "teleopChallengePoints"
      "autoCrossingPoints"
      "teleopDefensesBreached"
      "autoReachPoints"
      "position2"
      "capturePoints"
	"""
	def __init__(self, match_dict):
		self.real_data = match_dict
		self.level = match_dict["comp_level"]
		self.match_num = match_dict["match_number"]
		self.blue_alliance_performance = match_dict["score_breakdown"]["blue"]
		self.red_alliance_performance = match_dict["score_breakdown"]["red"]
		self.red = Alliance(match_dict["alliances"]["red"]["teams"][0],
							match_dict["alliances"]["red"]["teams"][1],
							match_dict["alliances"]["red"]["teams"][2])

		self.blue = Alliance(match_dict["alliances"]["blue"]["teams"][0],
							match_dict["alliances"]["blue"]["teams"][1],
							match_dict["alliances"]["blue"]["teams"][2])

	def get_red_alliance(self):
		return self.red

	def get_blue_alliance(self):
		return self.blue

	def get_blue_total(self):
		return self.blue_alliance_performance["totalPoints"]

	def get_red_total(self):
		return self.red_alliance_performance["totalPoints"]



get_match("2016cmp_f1m1")