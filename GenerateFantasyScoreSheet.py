import TBAconnection
import GenerateRosterLists
import os

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
		if not os.path.exists("data/fantasy/2017" + eventid):
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
				if info[6] == "True":
					rows[team].append("YES")
				else:
					rows[team].append("NO")
				if info[7] == "True":
					rows[team].append("YES")
				else:
					rows[team].append("NO")
		qual_file.close()

		if not os.path.exists(folder + "/on_alliances.txt"):
			continue
		alliance_file = open(folder + "/on_alliances.txt", "r")
		alliance_content = alliance_file.read().splitlines()
		on_alliance = False
		for line in alliance_content:
			if line == team:
				rows[team].append("YES")
				on_alliance = True
		if not on_alliance:
			rows[team].append("NO")
		alliance_file.close()

		if not os.path.exists(folder + "/alliance_captains.txt"):
			continue
		captain_file = open(folder + "/alliance_captains.txt", "r")
		captain_content = captain_file.read().splitlines()
		captain = False
		for line in captain_content:
			if line == team:
				rows[team].append("YES")
				captain = True
		if not captain:
			rows[team].append("NO")
		captain_file.close()

		elims_won = 0

		if not os.path.exists(folder + "/quarterfinals_winners.txt"):
			continue
		qf_file = open(folder + "/quarterfinals_winners.txt", "r")
		qf_content = qf_file.read().splitlines()
		qf = False
		for line in qf_content:
			if line == team:
				elims_won += 2
				rows[team].append("YES")
				qf = True
		if not qf:
			rows[team].append("NO")
		qf_file.close()

		if not os.path.exists(folder + "/semifinals_winners.txt"):
			continue
		sf_file = open(folder + "/semifinals_winners.txt", "r")
		sf_content = sf_file.read().splitlines()
		sf = False
		for line in sf_content:
			if line == team:
				elims_won += 2
				rows[team].append("YES")
				sf = True
		if not sf:
			rows[team].append("NO")
		sf_file.close()

		if not os.path.exists(folder + "/finals_winners.txt"):
			continue
		f_file = open(folder + "/finals_winners.txt", "r")
		f_content = f_file.read().splitlines()
		f = False
		for line in f_content:
			if line == team:
				elims_won += 2
				rows[team].append("YES")
				f = True
		if not f:
			rows[team].append("NO")
		f_file.close()

		if not os.path.exists(folder + "/quarterfinalseliminated.txt"):
			continue
		if not os.path.exists(folder + "/semifinalseliminated.txt"):
			continue
		if not os.path.exists(folder + "/finalseliminated.txt"):
			continue
		elim_file_qf = open(folder + "/quarterfinalseliminated.txt", "r")
		elim_file_sf = open(folder + "/semifinalseliminated.txt", "r")
		elim_file_f = open(folder + "/finalseliminated.txt", "r")
		elim_content_qf = elim_file_qf.read().splitlines()
		elim_content_sf = elim_file_sf.read().splitlines()
		elim_content_f = elim_file_f.read().splitlines()
		elim = False
		for line in elim_content_qf:
			if line == team:
				elims_won += 1
				rows[team].append("YES")
				elim = True
		for line in elim_content_sf:
			if line == team:
				elims_won += 1
				rows[team].append("YES")
				elim = True
		for line in elim_content_f:
			if line == team:
				elims_won += 1
				rows[team].append("YES")
				elim = True
		if not elim:
			rows[team].append("NO")
		elim_file_qf.close()
		elim_file_sf.close()
		elim_file_f.close()

		rows[team].append(elims_won)

	out_f = open(out_file, "w")
	for team in rows:
		for cell in rows[team]:
			out_f.write(str(cell) + ",")
		out_f.write("\n")
	out_f.close()