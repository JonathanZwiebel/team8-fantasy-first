import urllib2
import json
import math

def get_event_list(year):
	"""
	Method that will return a list of TBAEvents
	"""
	url = "http://www.thebluealliance.com/api/v2/events/" + str(year) + '?X-TBA-App-Id=frc8%3Afantasy-league%3Adev'
	request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'})
	data = urllib2.urlopen(request).read().decode('utf-8')
	jsonvar = json.loads(data)

	return_val = []
	for i in jsonvar:
		return_val.append(TBAEvent(i))

	return return_val

def get_event(eventKey):
	"""
	Method that returns data for one event
	"""	
	url = "http://www.thebluealliance.com/api/v2/event/" + eventKey + '?X-TBA-App-Id=frc8%3Afantasy-league%3Adev'
	request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'})
	data = urllib2.urlopen(request).read().decode('utf-8')
	jsonvar = json.loads(data)
	
	return TBAEvent(jsonvar)

def get_matches_with_teams(eventKey):
	"""
	Method that will return a list of TBAMatch
	"""
	url = "http://www.thebluealliance.com/api/v2/event/" + eventKey + "/matches" + '?X-TBA-App-Id=frc8%3Afantasy-league%3Adev'
	request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'})
	data = urllib2.urlopen(request).read().decode('utf-8')
	jsonvar = json.loads(data)

	return_val = []
	for i in jsonvar:
		return_val.append(FullTBAMatch(i))

	return return_val


def get_teams_at_event(eventKey):
	"""
	Method that will return a list of TBATeams
	"""
	url = "http://www.thebluealliance.com/api/v2/event/" + eventKey + "/teams" + '?X-TBA-App-Id=frc8%3Afantasy-league%3Adev'
	request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'})
	data = urllib2.urlopen(request).read().decode('utf-8')
	jsonvar = json.loads(data)

	return_val = []
	for i in jsonvar:
		return_val.append(FullTBATeam(i))

	return return_val

def get_match(matchkey):
	"""
	Method that will return a SuperMatch

	Note that the matchKey can be obtained using the key from the BasicTBAMatch object
	"""
	url = "http://www.thebluealliance.com/api/v2/match/" + matchkey + '?X-TBA-App-Id=frc8%3Afantasy-league%3Adev'
	request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'})
	data = urllib2.urlopen(request).read().decode('utf-8')
	jsonvar = json.loads(data)

	return FullTBAMatch(jsonvar)

def get_event_ranking(eventid):
	"""
	Method that will 
	return ranking data for an event
	"""
	url = "http://www.thebluealliance.com/api/v2/event/" + eventid + "/rankings" + '?X-TBA-App-Id=frc8%3Afantasy-league%3Adev'
	request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'})
	data = urllib2.urlopen(request).read().decode('utf-8')
	jsonvar = json.loads(data)

	return TBAQualRanking(jsonvar)

def get_event_awards(eventid):
	"""
	Method that will return an object that lists event Chairman's, Winners, and Finalists
	"""
	url = "http://www.thebluealliance.com/api/v2/event/" + eventid + "/awards" + '?X-TBA-App-Id=frc8%3Afantasy-league%3Adev'
	request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'})
	data = urllib2.urlopen(request).read().decode('utf-8')
	jsonvar = json.loads(data)

	return EventAwards(jsonvar)
	print jsonvar

award_numbers = {0 : "Chairman's", 1 : "Winners", 2 : "Finalists"}
class EventAwards:
	# Using numbers instead of award names because names change depending on event type
	award_winners = {}
	def __init__(self, event_awards):
		self.event_awards = event_awards
		for award in event_awards:
			award_number = award["award_type"]
			if award_numbers.has_key(award_number):
				award = award_numbers[award_number]
				print award
			

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

class TBAQualRanking(object):
	def __init__(self, qual_ranking_array):
		self.qual_ranking_array = qual_ranking_array

	def get_ranking(self):
		return self.qual_ranking_array

	def get_team_in_rank(self, rank):
		return self.qual_ranking_array[rank]

class TBAEvent(object):
	def __init__(self, event_dict):
		self.real_data = event_dict
		self.key = event_dict["key"]
		self.name = event_dict["name"]
		self.event_type_string = event_dict["event_type_string"]
		self.event_district_string = event_dict["event_district_string"]
		self.week = event_dict["week"]
		self.location = event_dict["location"]
		self.tba_alliances = event_dict["alliances"]
		self.official = event_dict["official"]

	def get_key(self):
		return self.key

	def get_name(self):
		return self.name

	def get_event_type(self):
		return self.event_type_string

	def get_event_district(self):
		return self.event_district_string

	def get_week(self):
		return self.week

	def get_location(self):
		return self.location

	def is_official(self):
		return self.official

	def get_alliances(self):
		return self.tba_alliances

	def get_alliances_lists(self):
		alliances_list = []
		for alliance in self.tba_alliances:
			alliances_list.append(alliance["picks"])
		return alliances_list

class FullTBATeam(object):
	"""
	  "website"
	  "name"
	  "locality"
	  "region"
	  "country_name"
	  "location"
	  "team_number"
	  "key"
	  "nickname"
	  "rookie_year"
	  "motto"
	"""	
	def __init__(self, team_dict):
		self.real_data = team_dict
		self.team_number = team_dict["team_number"]
		self.key = team_dict["key"]
		self.rookie_year = team_dict["rookie_year"]
		self.nickname = team_dict["nickname"]

	def get_number(self):
		return self.team_number

	def get_key(self):
		return self.key

	def get_nickname(self):
		return self.nickname

	def get_rookie_year(self):
		return self.rookie_year

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
		self.key = match_dict["key"].encode('ascii', 'ignore')
		self.level = match_dict["comp_level"]
		self.match_num = match_dict["match_number"]
		if str(match_dict["score_breakdown"]) == "None":
			self.bad = True
			return 
		self.bad = False
		self.blue_alliance_performance = match_dict["score_breakdown"]["blue"]
		self.red_alliance_performance = match_dict["score_breakdown"]["red"]
		self.red = Alliance(match_dict["alliances"]["red"]["teams"][0],
							match_dict["alliances"]["red"]["teams"][1],
							match_dict["alliances"]["red"]["teams"][2])

		self.blue = Alliance(match_dict["alliances"]["blue"]["teams"][0],
							match_dict["alliances"]["blue"]["teams"][1],
							match_dict["alliances"]["blue"]["teams"][2])

	def get_good(self):
		return not self.bad

	def get_key_as_displayable(self):
		display = self.key.split("_")[1]

		if display[0:2] == "qm":
			return display.split("qm")[1]
		else:
			return display

	def get_red_alliance(self):
		return self.red

	def get_blue_alliance(self):
		return self.blue

	def get_winner(self):
		if self.blue_alliance_performance["totalPoints"] > self.red_alliance_performance["totalPoints"]:
			return "blue"
		if self.blue_alliance_performance["totalPoints"] < self.red_alliance_performance["totalPoints"]:
			return "red"
		return "tie"

	def get_blue_total(self):
		return self.blue_alliance_performance["totalPoints"]

	def get_red_total(self):
		return self.red_alliance_performance["totalPoints"]

	def get_blue_teleop_boulders_high(self):
		return self.blue_alliance_performance["teleopBouldersHigh"]

	def get_red_teleop_boulders_high(self):
		return self.red_alliance_performance["teleopBouldersHigh"]

	def get_blue_teleop_boulders_low(self):
		return self.blue_alliance_performance["teleopBouldersLow"]

	def get_red_teleop_boulders_low(self):
		return self.red_alliance_performance["teleopBouldersLow"]

	def get_blue_auto_boulders_high(self):
		return self.blue_alliance_performance["autoBouldersHigh"]

	def get_red_auto_boulders_high(self):
		return self.red_alliance_performance["autoBouldersHigh"]

	def get_blue_teleop_points(self):
		return self.blue_alliance_performance["teleopPoints"]

	def get_red_teleop_points(self):
		return self.red_alliance_performance["teleopPoints"]

	def get_blue_auto_points(self):
		return self.blue_alliance_performance["autoPoints"]

	def get_red_auto_points(self):
		return self.red_alliance_performance["autoPoints"]

	def get_blue_rp(self):
		rp = 0
		if self.blue_alliance_performance["teleopDefensesBreached"]:
			rp += 1
		if self.blue_alliance_performance["teleopTowerCaptured"]:
			rp += 1
		if self.get_blue_total() > self.get_red_total():
			rp += 2
		elif self.get_blue_total() == self.get_red_total():
			rp += 1
		return rp

	def get_red_rp(self):
		rp = 0
		if self.red_alliance_performance["teleopDefensesBreached"]:
			rp += 1
		if self.red_alliance_performance["teleopTowerCaptured"]:
			rp += 1
		if self.get_red_total() > self.get_blue_total():
			rp += 2
		elif self.get_blue_total() == self.get_red_total():
			rp += 1
		return rp

	def get_blue_breach(self):
		if self.blue_alliance_performance["teleopDefensesBreached"]:
			return 1
		return 0

	def get_red_breach(self):
		if self.red_alliance_performance["teleopDefensesBreached"]:
			return 1
		return 0

	def get_blue_crossings(self):
		total = 0
		total += self.blue_alliance_performance["position1crossings"]
		total += self.blue_alliance_performance["position2crossings"]
		total += self.blue_alliance_performance["position3crossings"]
		total += self.blue_alliance_performance["position4crossings"]
		total += self.blue_alliance_performance["position5crossings"]
		return total
		
	def get_red_crossings(self):
		total = 0
		total += self.red_alliance_performance["position1crossings"]
		total += self.red_alliance_performance["position2crossings"]
		total += self.red_alliance_performance["position3crossings"]
		total += self.red_alliance_performance["position4crossings"]
		total += self.red_alliance_performance["position5crossings"]
		return total

	def get_blue_tower_strength(self):
		return self.red_alliance_performance["towerEndStrength"]

	def get_red_tower_strength(self):
		return self.blue_alliance_performance["towerEndStrength"]

	def get_blue_scale_points(self):
		return self.blue_alliance_performance["teleopScalePoints"]

	def get_red_scale_points(self):
		return self.red_alliance_performance["teleopScalePoints"]

	def get_blue_winning_margin(self):
		return self.blue_alliance_performance["totalPoints"] - self.red_alliance_performance["totalPoints"]

	def get_red_winning_margin(self):
		return self.red_alliance_performance["totalPoints"] - self.blue_alliance_performance["totalPoints"]

	def get_blue_high(self):
		return self.blue_alliance_performance["teleopBouldersHigh"] + self.blue_alliance_performance["autoBouldersHigh"]

	def get_red_high(self):
		return self.red_alliance_performance["teleopBouldersHigh"] + self.red_alliance_performance["autoBouldersHigh"]

	def get_blue_low(self):
		return self.blue_alliance_performance["teleopBouldersLow"] + self.blue_alliance_performance["autoBouldersLow"]

	def get_red_low(self):
		return self.red_alliance_performance["teleopBouldersLow"] + self.red_alliance_performance["autoBouldersLow"]
