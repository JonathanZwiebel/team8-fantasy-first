# This class generates text files with the list of teams attending all event
#
# Author: Jonathan Zwiebel
# Version: 28 December 2016

import TBAconnection 
import TeamList


def generate_teamlists(year):
	events = TBAconnection.get_event_list(year)

	for event in events:
		TeamList.generate_teamlist(event.get_key(), str(event.get_event_type()), event.get_name())

generate_teamlists(2017)