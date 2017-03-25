import TBAconnection
import GenerateRosterLists

def generate_fantasy_score_sheet(roster_file, roster_date, week, out_file):
	rows = {}	

	rosters = GenerateRosterLists.generate_roster_lists(roster_file)
	for roster in rosters:
		for i in range(1, len(roster)):
			bi = [roster[i], roster[0]]
			basic_info = "data/" + roster_date + "/" + roster[0] + "-" + roster_date + ".csv"
			bi_file = open(basic_info, "r")
			content = bi_file.read().splitlines()
			for line in content:
				info = line.split(",")
				if info[0] == roster[i]:
					eventid = info[week + 2]
					bi.append(eventid)
					bi.append(info[1])
					event = TBAconnection.get_event("2017" + eventid)
					bi.append(event.get_name())
			bi_file.close()
			rows[roster[i]] = bi

	for team in rows:
		eventid = rows[team][2]
		if eventid != "mndu2":
			continue
		folder = "data/fantasy/2017" + eventid

		qual_file = open(folder + "/qual_data.csv", "r")

		qual_content = qual_file.read().splitlines()
		for line in qual_content:
			info = line.split(",")
			if info[0] == team:
				rows[team].append(info[3])
				record = info[4].split("-")
				rows[team].append(record[0])
				rows[team].append(record[1])
				rows[team].append(record[2])
				rows[team].append(info[2])


	out_f = open(out_file, "w")
	for team in rows:
		for cell in rows[team]:
			out_f.write(str(cell) + ",")
		out_f.write("\n")
	out_f.close()