# This class generates files to show different events
#
# Author: Jonathan Zwiebel
# Version: 30 December 2016

import TBAconnection 
import TeamList


def generate_eventlist(year):
	events = TBAconnection.get_event_list(year)

	filename = "data/eventlist.txt"
	file = open(filename, 'w')

	file.write("Events for " + str(year))
	for event in events:
		file.write(event.get_name() + "\n")

	file.close()

def generate_eventsheet(year):
	events = TBAconnection.get_event_list(year)

	filename = "data/eventsheet" + str(year) + ".csv"
	file = open(filename, 'w')

	for event in events:
		file.write(event.get_key() + ",")
		file.write("\"" + event.get_name() + "\",")
		file.write("\"" + event.get_location() + "\",")
		week = event.get_week()
		if week > -1:
			file.write(str(week + 1) + ",")
		else:
			file.write("cmp,")
		file.write(event.get_event_type() + ",")
		file.write(str(event.get_event_district()) + "\n")

	file.close()

generate_eventsheet(2017)