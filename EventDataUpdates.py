# This class will handle the transformation from raw API data to Team 8 Fantasy FIRST metrics
# Author: Jonathan Zwiebel
# Version: 1 January 2017
# TODO: Add playing rosters to data

import TBAconnection
import EventUpdates
import os
import operator

points_for_rank = [45, 35, 25, 20, 15, 10, 7, 3]

# Gets general data from an event such as name, location, and teams. Creates a folder
# for the event.
# To be run before an event begins
def initial_data_update(eventid):
	event = TBAconnection.get_event(eventid)

	output = "data/fantasy/" + eventid
	if not os.path.exists(output):
		EventUpdates.initial_update(eventid)
		os.makedirs(output)

	""" 
	Writes and information file in the following format:

	Event Name
	Event Type
	Associated District
	"""
	f = open(output + "/information.txt", "w")
	f.write(event.get_name() + "\n")
	f.write(event.get_event_type() + "\n")
	f.write(str(event.get_event_district()) + "\n")
	f.close()

# Gets qualification data from an event, calculated fantasy points, and places 
# a csv inside that event's data folder matching teams to data including fantasy points
# To be run at the end of qualification matches
def quals_data_update(eventid):
	qual_ranking = TBAconnection.get_event_ranking(eventid)

	output = "data/fantasy/" + eventid
	f = open(output + "/qual_data.csv", "w")

	for i in range(len(qual_ranking.get_ranking()) - 1):
		team = qual_ranking.get_team_in_rank(i + 1)

		points = float(team[2])

		if i < 8:
			points += points_for_rank[i]

		dash_index = team[7].index('-')
		wins = int(team[7][:dash_index])
		plays = int(team[8])

		if plays - wins == 0:
			points += 14
		elif plays - wins <= 2:
			points += 5

		# Team, Fantasy Points, RP, Record
		f.write(str(team[1]) + "," + str(points) + "," + str(team[2]) + "," + str(team[7]) + "\n")

	f.close()

	EventUpdates.quals_update(eventid, output)

def alliance_selection_data_update(eventid):
	event = TBAconnection.get_event(eventid)
	alliances_lists = event.get_alliances_lists()

	output = "data/fantasy/" + eventid
	f = open(output + "/alliance_selection_data.csv", "w")

	# A team appears here if they were selected onto an alliance
	alliance_data = open(output + "/on_alliances.txt", "w")

	for rank in range(len(alliances_lists)):
		f.write(str(rank + 1))
		for team in alliances_lists[rank]:
			f.write("," + str(team))
			alliance_data.write(team[3:] + "\n")
		f.write("\n")

	alliance_data.close()
	f.close()

	EventUpdates.alliance_selection_update(eventid, output)

# Section should be one of: eights, quarterfinals, semifinals, finals
section_count = {"eights":8, "quarterfinals":4, "semifinals":2, "finals":1}
section_id = {"eights":"ef", "quarterfinals":"qf", "semifinals":"sf", "finals":"f"}
def elims_section_data_update(eventid, section):
	output = "data/fantasy/" + eventid
	f = open(output + "/" + section + "_data.csv", "w")

	elim_scoring = open(output + "/" + section + "_winners.csv", "w")

	winners = {}
	losers = {}
	tiebreak = {}
	for i in range(section_count[section]):
		match1 = TBAconnection.get_match(eventid + "_" + section_id[section] + str(i+1) + "m1")
		match1_winner = match1.get_winner()
		match2 = TBAconnection.get_match(eventid + "_" + section_id[section] + str(i+1) + "m2")
		match2_winner = match2.get_winner()
		if match1_winner == match2_winner:
			tiebreak[i] = False
			if match1_winner == "red":
				winners[i] = match2.get_red_alliance().get_teams()
				losers[i] = match2.get_blue_alliance().get_teams()
			elif match1_winner == "blue":
				winners[i] = match2.get_blue_alliance().get_teams()
				losers[i] = match2.get_red_alliance().get_teams()
			else:
				print "tied match error"
		else:
			tiebreak[i] = True
			match3 = TBAconnection.get_match(eventid + "_" + section_id[section] + str(i+1) + "m3")
			match3_winner = match3.get_winner()
			if match3_winner == "red":
				winners[i] = match3.get_red_alliance().get_teams()
				losers[i] = match3.get_blue_alliance().get_teams()
			elif match3_winner == "blue":
				winners[i] = match3.get_blue_alliance().get_teams()
				losers[i] = match3.get_red_alliance().get_teams()
			else:
				print "tied match error"	

	# Match, Winning alliance (3), Losing alliance (3), Tiebreak
	for i in range(section_count[section]):
		f.write(str(i) + ",")
		for j in range(len(winners[i])):
			f.write(winners[i][j] + ",")
			elim_scoring.write(winners[i][j][3:] + "\n")
		for j in range(len(losers[i])):
			f.write(losers[i][j] + ",")
		f.write(str(tiebreak[i]) + "\n")
	f.close()
	elim_scoring.close()

	EventUpdates.elims_section_update(eventid, section, output)

# To be run at the end of an event
# Calculates the earned fantasy points of all teams
def final_data_update(eventid):
	fantasy_points = {}
	
	data = "data/fantasy/" + eventid
	quals_data = open(data +"/qual_data.csv", "r")
	on_alliance_data = open(data + "/on_alliances.txt", "r")
	qf_winners_data = open(data + "/quarterfinals_winners.csv", "r")    
	sf_winners_data = open(data + "/semifinals_winners.csv", "r")  
	f_winners_data = open(data + "/finals_winners.csv", "r")  
	fantasy_point_data = open(data + "/fantasy_point_data.csv", "w")

	with quals_data:
		quals_content = quals_data.read().splitlines()
	for team in quals_content:
		comma1 = team.index(",")
		comma2 = team.index(",", comma1+1)
		fantasy_points[team[:comma1]] = float(team[comma1+1:comma2])

	with on_alliance_data:
		on_alliance_content = on_alliance_data.read().splitlines()
	for team in on_alliance_content:
		fantasy_points[team] += 5

	with qf_winners_data:
		qf_winners_content = qf_winners_data.read().splitlines()
	for team in qf_winners_content:
		fantasy_points[team] += 10

	with sf_winners_data:
		sf_winners_content = sf_winners_data.read().splitlines()
	for team in sf_winners_content:
		fantasy_points[team] += 20

	with f_winners_data:
		f_winners_content = f_winners_data.read().splitlines()
	for team in f_winners_content:
		fantasy_points[team] += 40

	sorted_fantasy_points = sorted(fantasy_points.items(), key=operator.itemgetter(1), reverse=True)

	for team in sorted_fantasy_points:
		fantasy_point_data.write(str(team[0]) + "," + str(team[1]) + "\n")

	quals_data.close()
	on_alliance_data.close()
	qf_winners_data.close()
	sf_winners_data.close()
	f_winners_data.close()
	fantasy_point_data.close()

	EventUpdates.final_update(eventid, data)

#initial_data_update("2016casj")
#quals_data_update("2016casj")
#alliance_selection_data_update("2016casj")
#elims_section_data_update("2016casj", "quarterfinals")
#elims_section_data_update("2016casj", "semifinals")
#elims_section_data_update("2016casj", "finals")
final_data_update("2016casj")