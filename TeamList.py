# This class generates text files with the list of teams attending an event
#
# Author: Jonathan Zwiebel
# Version: 28 December 2016

import TBAconnection 

# Receieves data from TBA API
eventid = "2017cave"
teams =  TBAconnection.get_teams_at_event(eventid)

filename = "data/" + eventid + ".txt"
file = open(filename, "w")


for team in teams:
	file.write(str(team.get_number()))
	file.write("\n")

file.close()