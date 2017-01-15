# This class compares the number of years a team has been around to its performance
# This comparions uses years prior to and including 2016 vs average qualification RP in 2016

import TBAconnection


def extract_average_rp(year):
	events = TBAconnection.get_event_list(year)

	# Team Number : [Total RP, Qual Matches Played]
	data = {}

	valid_event_types = {"District", "Regional", "District Championship", "Championship Division"}

	for event in events:
		if not str(event.get_event_type()) in valid_event_types:
			print "Discarding " + str(event.get_event_type()) + " event"
			continue

		qual_ranking = TBAconnection.get_event_ranking(event.get_key())

		for i in range(len(qual_ranking.get_ranking()) - 1):
			team = qual_ranking.get_team_in_rank(i + 1)

			number = int(team[1])
			total_rp = float(team[2])
			matches = int(team[8])

			if number in data:
				data[number][0] += total_rp
				data[number][1] += matches
			else:
				data[number] = []
				data[number].append(total_rp)
				data[number].append(matches)

		print "Done with " + event.get_name()
		
	f = open("data/teamdata/average-rp.csv", "w")

	for team in data:
		f.write(str(team) + "," + str(data[team][0] / data[team][1]) + "\n")

	f.close()

def extract_rookie_year(year):
	events = TBAconnection.get_event_list(year)

	# Team Number : [Total RP, Qual Matches Played]
	data = {}

	valid_event_types = {"District", "Regional", "District Championship", "Championship Division"}

	for event in events:
		if not str(event.get_event_type()) in valid_event_types:
			print "Discarding " + str(event.get_event_type()) + " event"
			continue

		teams = TBAconnection.get_teams_at_event(event.get_key())

		for team in teams:
			if not team.get_number() in data:
				data[team.get_number()] = team.get_rookie_year()
		print "Done with " + event.get_name()


	f = open("data/teamdata/rookie-year.csv", "w")

	for team in data:
		f.write(str(team) + "," + str(data[team]) + "\n")

	f.close()

def extract_region(year):
	events = TBAconnection.get_event_list(year)

	# Team Number : [Total RP, Qual Matches Played]
	data = {}

	valid_event_types = {"District", "Regional", "District Championship", "Championship Division"}

	for event in events:
		if not str(event.get_event_type()) in valid_event_types:
			continue

		teams = TBAconnection.get_teams_at_event(event.get_key())

		for team in teams:
			if not team.get_number() in data:
				data[team.get_number()] = team.get_region()
		print "Done with " + event.get_name() + " | " + event.get_event_type()


	f = open("data/teamdata/region.csv", "w")

	for team in data:
		f.write(str(team) + "," + data[team].encode('ascii', 'ignore') + "\n")

	f.close()

def match_stats(file1, file2, file3, fileout):
	f1data = {}
	f2data = {}
	f3data = {}

	f1 = open(file1, "r")
	content1 = f1.read().splitlines()
	for team in content1:
		comma = team.index(",")
		f1data[team[:comma]] = team[comma+1:]
	f1.close()

	f2 = open(file2, "r")
	content2 = f2.read().splitlines()
	for team in content2:
		comma = team.index(",")
		f2data[team[:comma]] = team[comma+1:]
	f2.close()


	f3 = open(file3, "r")
	content3 = f3.read().splitlines()
	for team in content3:
		comma = team.index(",")
		f3data[team[:comma]] = team[comma+1:]
	f3.close()

	fout = open(fileout, "w")

	for team_number in f1data:
		fout.write(team_number + "," + f1data[team_number] + "," + f2data[team_number] + "," + f3data[team_number] + "\n")

	fout.close()

#extract_region(2016)
match_stats("data/teamdata/average-rp.csv", "data/teamdata/rookie-year.csv", "data/teamdata/region.csv","data/teamdata/rp-year-region.csv")