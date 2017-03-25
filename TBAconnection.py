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


def get_team(teamNumber):
	"""
	Method that returns data for one event
	"""	
	url = "http://www.thebluealliance.com/api/v2/team/" + "frc" + str(teamNumber) + '?X-TBA-App-Id=frc8%3Afantasy-league%3Adev'
	request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'})
	data = urllib2.urlopen(request).read().decode('utf-8')
	jsonvar = json.loads(data)
	
	return FullTBATeam(jsonvar)

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

def get_statistics(eventid):
	url = "http://www.thebluealliance.com/api/v2/event/" + eventid + "/stats" + '?X-TBA-App-Id=frc8%3Afantasy-league%3Adev'
	request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'})
	data = urllib2.urlopen(request).read().decode('utf-8')
	jsonvar = json.loads(data)

	return jsonvar

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


def get_distrct_history(team_number):
	url = "http://www.thebluealliance.com/api/v2/team/" + "frc" + str(team_number) + "/history/districts" + '?X-TBA-App-Id=frc8%3Afantasy-league%3Adev'
	request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'})
	data = urllib2.urlopen(request).read().decode('utf-8')
	jsonvar = json.loads(data)

	return jsonvar

def get_team_events(team_number, year):
	url = "http://www.thebluealliance.com/api/v2/team/" + "frc" + str(team_number) + "/" + str(year) + "/events" + '?X-TBA-App-Id=frc8%3Afantasy-league%3Atesting'
	request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'})
	data = urllib2.urlopen(request).read().decode('utf-8')
	jsonvar = json.loads(data)

	return_val = []
	for i in jsonvar:
		return_val.append(TBAEvent(i))
	return return_val

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

	def as_csv_string(self):
		return ",".join(self.teams)

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
		if self.key == "2017cmptx":
			return 8

		if self.key == "2017cmpmo":
			return 9

		if not isinstance(self.week, int):
			return -1

		return int(self.week) + 1

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
		self.region = team_dict["region"]
		self.locality = team_dict["locality"]

	def get_region(self):
		return self.region

	def get_number(self):
		return self.team_number

	def get_key(self):
		return self.key

	def get_nickname(self):
		return self.nickname

	def get_rookie_year(self):
		return self.rookie_year

	def get_locality(self):
		return self.locality

class FullTBAMatch(object):
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

	def get_key(self):
		return self.key

	def get_level(self):
		return self.level

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

	# Sort levels: Total Points, Foul Points
	def get_full_winner(self):
		if self.blue_alliance_performance["totalPoints"] > self.red_alliance_performance["totalPoints"]:
			return "blue"
		if self.blue_alliance_performance["totalPoints"] < self.red_alliance_performance["totalPoints"]:
			return "red"
		if self.blue_alliance_performance["foulPoints"] > self.red_alliance_performance["foulPoints"]:
			return "blue"
		if self.blue_alliance_performance["foulPoints"] < self.red_alliance_performance["foulPoints"]:
			return "red"
		if self.blue_alliance_performance["autoPoints"] > self.red_alliance_performance["autoPoints"]:
			return "blue"
		if self.blue_alliance_performance["autoPoints"] < self.red_alliance_performance["autoPoints"]:
			return "red"
		if self.blue_alliance_performance["teleopRotorPoints"] + self.blue_alliance_performance["autoRotorPoints"] > self.red_alliance_performance["teleopRotorPoints"] + self.red_alliance_performance["autoRotorPoints"]:
			return "blue"
		if self.blue_alliance_performance["teleopRotorPoints"] + self.blue_alliance_performance["autoRotorPoints"] < self.red_alliance_performance["teleopRotorPoints"] + self.red_alliance_performance["autoRotorPoints"]:
			return "red"
		if self.blue_alliance_performance["teleopTakeoffPoints"] > self.red_alliance_performance["teleopTakeoffPoints"]:
			return "blue"
		if self.blue_alliance_performance["teleopTakeoffPoints"] < self.red_alliance_performance["teleopTakeoffPoints"]:
			return "red"
		if self.blue_alliance_performance["teleopFuelPoints"] + self.blue_alliance_performance["autoFuelPoints"] > self.red_alliance_performance["teleopFuelPoints"] + self.red_alliance_performance["autoFuelPoints"]:
			return "blue"
		if self.blue_alliance_performance["teleopFuelPoints"] + self.blue_alliance_performance["autoFuelPoints"] < self.red_alliance_performance["teleopFuelPoints"] + self.red_alliance_performance["autoFuelPoints"]:
			return "red"
		return "tie"

	def get_blue_total(self):
		return self.blue_alliance_performance["totalPoints"]

	def get_red_total(self):
		return self.red_alliance_performance["totalPoints"]

	def get_blue_teleop_points(self):
		return self.blue_alliance_performance["teleopPoints"]

	def get_red_teleop_points(self):
		return self.red_alliance_performance["teleopPoints"]

	def get_blue_auto_points(self):
		return self.blue_alliance_performance["autoPoints"]

	def get_red_auto_points(self):
		return self.red_alliance_performance["autoPoints"]

	def get_blue_winning_margin(self):
		return self.blue_alliance_performance["totalPoints"] - self.red_alliance_performance["totalPoints"]

	def get_red_winning_margin(self):
		return self.red_alliance_performance["totalPoints"] - self.blue_alliance_performance["totalPoints"]