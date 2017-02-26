import TBAconnection

teams_per_roster = 12

def generate(location, date):
	filein = location + "/" + date + "/rosters-" + date + ".csv"
	f = open(filein, "r")
	rosters_str = f.read().splitlines()
	rosters = {}

	for roster_str in rosters_str:
		teams = []
		counted = 0
		last_comma_index = roster_str.index(",")
		name = roster_str[:last_comma_index]

		while(counted < teams_per_roster - 1):
			next_comma_index = roster_str.index(",", last_comma_index + 1)
			teams.append(int(roster_str[last_comma_index + 1:next_comma_index]))
			last_comma_index = next_comma_index
			counted = counted + 1
		teams.append(int(roster_str[last_comma_index + 1:]))
		rosters[name] = teams

	for roster in rosters:
		out = location + "/" + date + "/" + roster + "-" + date + ".csv"
		file_out = open(out, "w")

		for team in rosters[roster]:
			events_on_week = {}
			events = TBAconnection.get_team_events(team, 2017)
			for event in events:
				week = event.get_week()
				key = event.get_key()
				events_on_week[week] = key
			print events_on_week
			full_team = TBAconnection.get_team(team)
			district_data = TBAconnection.get_distrct_history(team)
			if "2017" in district_data:
				district = district_data["2017"][4:]
			else:
				district = "None"
			name = full_team.get_nickname()

			file_out.write(str(team) + "," + name + "," + district)
			for i in range(1, 10):
				file_out.write(",")
				if i in events_on_week:
					file_out.write(events_on_week[i][4:])
			file_out.write("\n")
		file_out.close()



generate("C:/users/user/git/tba-stats/data", "feb25")