# This class generates text files with the list of teams attending an event
#
# Author: Jonathan Zwiebel
# Version: 28 December 2016

import TBAconnection 

def generate_teamlist(eventid, header=""):
	teams =  TBAconnection.get_teams_at_event(eventid)

	filename = "data/teamlists/" + eventid + ".txt"
	file = open(filename, "w")

	file.write(header + "\n")
	for team in teams:
		file.write(str(team.get_number()))
		file.write("\n")

	file.close()

generate_teamlist("2017cave")
generate_teamlist("2017casj")