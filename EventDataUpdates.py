# This class will handle the transformation from raw API data to Team 8 Fantasy FIRST metrics
# Author: Jonathan Zwiebel
# Version: 1 January 2017
# TODO: Add playing rosters to data

import TBAconnection
import EventUpdates
import os

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

	for rank in range(len(alliances_lists)):
		f.write(str(rank + 1))
		for team in alliances_lists[rank]:
			f.write("," + str(team))
		f.write("\n")

	f.close()

	EventUpdates.alliance_selection_update(eventid, output)

initial_data_update("2016new")
quals_data_update("2016new")
alliance_selection_data_update("2016new")