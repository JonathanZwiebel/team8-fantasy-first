# This class will contain many functions for getting comprehensive data on all 
# teams competing in a year. It is meant to be used to assist in Fantasy FIRST 
# team selection. 

import TBAconnection

legal_event_types = {"District", "Regional", "District Championship"}
official_event_types = {"District", "Regional", "District Championship", "Championship Division"}


def extract_teams_and_events(year):
	events = TBAconnection.get_event_list(year)

	blank_events = ["-","-","-","-","-","-","-","-"]
	teams_to_events = {}

	for event in events:
		event_type = event.get_event_type()
		if not event_type in legal_event_types:
			print "Discarding " + event_type + " event"
			continue
		else:
			print "Extracing teams from " + event.get_name()

		week = int(event.get_week())
		key = event.get_key()

		teams = TBAconnection.get_teams_at_event(event.get_key())
		for team in teams:
			number = team.get_number()
			if number in teams_to_events:
				teams_to_events[number][week] = key[4:]
			else:
				teams_to_events[number] = blank_events[:]
				teams_to_events[number][week] = key[4:]


	output = "data/teamdata/teamsheets"
	filename = output + "/teams_to_events.csv"
	file = open(filename, "w")

	for team_number in teams_to_events:
		file.write(str(team_number))
		for week in range(8):
			file.write("," + teams_to_events[team_number][week])
		file.write("\n")

	file.close()

def from_teams_extract_basic_info(infopage):
	file = open(infopage, "r")
	content = file.read().splitlines()
	file.close()

	output = "data/teamdata/teamsheets"
	filename = output + "/teams_to_info.csv"
	out_file = open(filename, "w")

	for teams_to_event in content:
		comma = teams_to_event.index(",")
		team_number = teams_to_event[:comma]

		print("Getting data for team number " + team_number)
		team = TBAconnection.get_team(team_number)
		locality = team.get_locality()
		rookie_year = team.get_rookie_year()
		region = team.get_region()
		nickname = team.get_nickname()

		out_file.write(str(team_number) + ",\"" + locality.encode('ascii', 'ignore') + "\"," + str(rookie_year) + "," + region.encode('ascii', 'ignore') + ",\"" + nickname.encode('ascii', 'ignore') + "\"\n")

	out_file.close()

def from_teams_extract_district_info(infopage, year):
	file = open(infopage, "r")
	content = file.read().splitlines()
	file.close()


	output = "data/teamdata/teamsheets"
	filename = output + "/teams_to_districts.csv"
	out_file = open(filename, "w")

	for teams_to_event in content:
		comma = teams_to_event.index(",")
		team_number = teams_to_event[:comma]

		print("Getting data for team number " + team_number)
		data = TBAconnection.get_distrct_history(team_number)
		if str(year) in data:
			out_file.write(str(team_number) + "," + "district" + "," + data[str(year)][4:] + "\n")
		else:
			out_file.write(str(team_number) + "," + "regional" + "," + "none" + "\n")

	out_file.close()

def from_teams_extract_tba_statistics(infopage, year):
	file = open(infopage, "r")
	content = file.read().splitlines()
	file.close()
	teams_to_stats_max = {}
	teams_to_stats_min = {}
	for teams_to_event in content:
		comma = teams_to_event.index(",")
		team_number = teams_to_event[:comma]
		teams_to_stats_max[team_number] = ["-","-","-"]
		teams_to_stats_min[team_number] = ["-","-","-"]

	events = TBAconnection.get_event_list(year)
	for event in events:
		event_type = event.get_event_type()
		if not event_type in official_event_types:
			print "Discarding " + event_type + " event"
			continue
		else:
			print "Getting statistics for " + event.get_name()
		statistics = TBAconnection.get_statistics(event.get_key())

		oprs = statistics["oprs"]
		ccwms = statistics["ccwms"]
		dprs = statistics["dprs"]

		for team in oprs:
			if not team in teams_to_stats_max:
				continue

			opr = float(oprs[str(team)])
			ccwm = float(ccwms[str(team)])
			dpr = float(dprs[str(team)])

			if teams_to_stats_max[team][0] == "-":
				teams_to_stats_max[team] = [opr, ccwm, dpr]
				teams_to_stats_min[team] = [opr, ccwm, dpr]
			else:
				if opr > teams_to_stats_max[team][0]:
					teams_to_stats_max[team][0] = opr
				if ccwm > teams_to_stats_max[team][1]:
					teams_to_stats_max[team][1] = ccwm
				if dpr > teams_to_stats_max[team][2]:
					teams_to_stats_max[team][2] = dpr
				if opr < teams_to_stats_min[team][0]:
					teams_to_stats_min[team][0] = opr
				if ccwm < teams_to_stats_min[team][1]:
					teams_to_stats_min[team][1] = ccwm
				if dpr < teams_to_stats_min[team][2]:
					teams_to_stats_min[team][2] = dpr

	output = "data/teamdata/teamsheets"
	filename = output + "/teams_to_stats.csv"
	out_file = open(filename, "w")

	for team in teams_to_stats_max:
		out_file.write(str(team) + ",")
		for i in range(3):
			out_file.write(str(teams_to_stats_max[team][i]) + ",")
			out_file.write(str(teams_to_stats_min[team][i]) + ",")
		out_file.write("\n")
	out_file.close()


def from_teams_extract_csv_stats(infopage, csvpage):
	file = open(infopage, "r")
	content = file.read().splitlines()
	file.close()

	csv_file = open(csvpage, "r")
	csv_content = csv_file.read().splitlines()
	csv_file.close()

	output = "data/teamdata/teamsheets"
	filename = output + "/teams_to_csv_stats.csv"
	out_file = open(filename, "w")

	teams_to_csv_stats = {}

	for csv_line in csv_content:
		comma1 = csv_line.index(",")
		comma2 = csv_line.index(",", comma1 + 1)
		comma3 = csv_line.index(",", comma2 + 1)

		team_number = csv_line[:comma1]
		stat_2014 = csv_line[comma1 + 1:comma2]
		stat_2015 = csv_line[comma2 + 1:comma3]
		stat_2016 = csv_line[comma3 + 1:]

		teams_to_csv_stats[team_number] = [stat_2014, stat_2015, stat_2016]

	for teams_to_event in content:
		comma = teams_to_event.index(",")
		team_number = teams_to_event[:comma]

		print("Extracting data for team number " + team_number)

		if not team_number in teams_to_csv_stats:
			out_file.write(str(team_number) + ",-,-,-\n")
		else:
			out_file.write(str(team_number) + "," + teams_to_csv_stats[team_number][0] + "," + teams_to_csv_stats[team_number][1] + "," + teams_to_csv_stats[team_number][2] + "\n")

	out_file.close()