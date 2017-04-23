# This class will handle the transformation from raw API data to Team 8 Fantasy FIRST metrics
# Author: Jonathan Zwiebel
# Version: 1 January 2017
# TODO: Add playing rosters to data

import TBAconnection
import EventUpdates
import os
import operator
import GenerateRosterLists

points_for_rank = [45, 35, 25, 20, 15, 10, 7, 3]

# Gets general data from an event such as name, location, and teams. Creates a folder
# for the event.
# To be run before an event begins
def initial_data_update(eventid, to_slack = True):
	event = TBAconnection.get_event(eventid)

	output = "data/fantasy/" + eventid
	if not os.path.exists(output):
		if to_slack:
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
def quals_data_update(eventid, roster_file, to_slack = False):
	qual_ranking = TBAconnection.get_event_ranking(eventid)

	output = "data/fantasy/" + eventid
	f = open(output + "/qual_data.csv", "w")
	bp_f = open(output + "/bonus_point_data.csv", "w")
	high_scores_txt = open(output + "/high_scores.txt", "w")
	winning_margins_txt = open(output + "/winning_margins.txt", "w")

	matches = TBAconnection.get_matches_with_teams(eventid)

	highest_score = -1
	highest_wm = -1

	high_score_alliances = {}
	highest_wm_alliances = {}

	for match in matches:
		if match.get_level() != "qm" or not match.get_good():
			continue

		match_id = match.get_key()

		blue_total = match.get_blue_total()
		red_total = match.get_red_total()

		if blue_total >= highest_score:
			if blue_total > highest_score:
				high_score_alliances = {}
			highest_score = blue_total
			high_score_alliances[match_id] = match.get_blue_alliance()
		if red_total >= highest_score:
			if red_total > highest_score:
				high_score_alliances = {}
			highest_score = red_total
			high_score_alliances[match_id] = match.get_red_alliance()

		if blue_total - red_total >= highest_wm:
			if blue_total - red_total > highest_wm:
				highest_wm_alliances = {}
			highest_wm = blue_total - red_total
			highest_wm_alliances[match_id] = match.get_blue_alliance()
		if red_total - blue_total >= highest_wm:
			if red_total - blue_total > highest_wm:
				highest_wm_alliances = {}
			highest_wm = red_total - blue_total
			highest_wm_alliances[match_id] = match.get_red_alliance()

	print "High score of " + str(highest_score) + " by teams "
	for alliance in high_score_alliances:
		print high_score_alliances[alliance].as_string() + ","
	print "Highest WM of " + str(highest_wm) + " by teams " 
	for alliance in highest_wm_alliances:
		print highest_wm_alliances[alliance].as_string() + ","

	for alliance in high_score_alliances:
		bp_f.write(high_score_alliances[alliance].as_csv_string())
	bp_f.write("\n")
	for alliance in highest_wm_alliances:
		bp_f.write(highest_wm_alliances[alliance].as_csv_string())
	bp_f.close()

	hs_teams = []
	wm_teams = []

	for alliance in high_score_alliances:
		for hs_team in high_score_alliances[alliance].get_teams():
			hs_teams.append(hs_team[3:])
			high_scores_txt.write(hs_team[3:] + "\n")

	for alliance in highest_wm_alliances:
		for wm_team in highest_wm_alliances[alliance].get_teams():
			wm_teams.append(wm_team[3:])
			winning_margins_txt.write(wm_team[3:] + "\n")

	high_scores_txt.close()
	winning_margins_txt.close()

	print hs_teams
	print wm_teams

	for i in range(len(qual_ranking.get_ranking()) - 1):
		team = qual_ranking.get_team_in_rank(i + 1)
		dash_index = team[8].index('-')
		wins = int(team[8][:dash_index])
		plays = int(team[9])

		rp = round((plays) * float(team[2]))
		rp_points = 1.5 * rp

		high_score = False
		winning_margin = False

		if str(team[1]) in hs_teams:
			high_score = True
		if str(team[1]) in wm_teams:
			winning_margin = True

		if i < 8:
			seed_points = points_for_rank[i]
		else:
			seed_points = 0

		if plays - wins == 0:
			record_points = 11
			record_bonus = "big"
		elif plays - wins <= 2:
			record_points = 5
			record_bonus = "small"
		else:
			record_points = 0
			record_bonus = "none"

		bonus_points = 0
		if winning_margin:
			bonus_points += 3
		if high_score:
			bonus_points += 3

		points = rp_points + seed_points + record_points + bonus_points

		# Team, Fantasy Points, Ranking, RP, Record, HS, WM
		f.write(str(team[1]) + "," + str(points) + "," + str((i + 1)) + "," + str(rp) + "," + str(team[8]) + "," + record_bonus + "," + str(winning_margin) + "," + str(high_score) + "\n")
	f.close()

	if to_slack:
		EventUpdates.quals_update(eventid, output, roster_file, highest_score, highest_wm)

def alliance_selection_data_update(eventid, roster_file, to_slack = False):
	event = TBAconnection.get_event(eventid)
	alliances_lists = event.get_alliances_lists()

	output = "data/fantasy/" + eventid
	f = open(output + "/alliance_selection_data.csv", "w")
	alliance_data = open(output + "/on_alliances.txt", "w")
	captains_data = open(output + "/alliance_captains.txt", "w")

	for rank in range(len(alliances_lists)):
		f.write(str(rank + 1))
		captains_data.write(alliances_lists[rank][0][3:] + "\n")
		for team in alliances_lists[rank]:
			f.write("," + str(team))
			alliance_data.write(team[3:] + "\n")
		f.write("\n")

	captains_data.close()
	alliance_data.close()
	f.close()

	if to_slack:
		EventUpdates.alliance_selection_update(eventid, output, roster_file)

# Section should be one of: eights, quarterfinals, semifinals, finals
section_count = {"eights":8, "quarterfinals":4, "semifinals":2, "finals":1}
section_id = {"eights":"ef", "quarterfinals":"qf", "semifinals":"sf", "finals":"f"}
def elims_section_data_update(eventid, section, roster_file, to_slack = False):
	output = "data/fantasy/" + eventid

	f = open(output + "/" + section + "_data.csv", "w")
	elim_scoring = open(output + "/" + section + "_winners.txt", "w")

	winners = {}
	losers = {}
	eliminated = open(output + "/" + section + "eliminated.txt", "w")

	wins_by_winner = {}
	overall_winner = {}
	overall_loser = {}

	for i in range(section_count[section]):
		wins_by_winner[i] = {"red":0, "blue":0, "tie":0}

		match1 = TBAconnection.get_match(eventid + "_" + section_id[section] + str(i+1) + "m1")
		match2 = TBAconnection.get_match(eventid + "_" + section_id[section] + str(i+1) + "m2")
		if section == "f":
			match1_winner = match1.get_winner()
			match2_winner = match2.get_winner()
		else:
			match1_winner = match1.get_full_winner()
			match2_winner = match2.get_full_winner()

		wins_by_winner[i][match1_winner] += 1
		wins_by_winner[i][match2_winner] += 1
		latest_match = match2


		games_counted = 2

		while wins_by_winner[i]["red"] < 2 and wins_by_winner[i]["blue"] < 2:
			tiebreak_match = TBAconnection.get_match(eventid + "_" + section_id[section] + str(i+1) + "m" + str(games_counted + 1))
			winner = tiebreak_match.get_full_winner()
			wins_by_winner[i][winner] += 1
			games_counted += 1
			latest_match = tiebreak_match

		print "RED: " + str(wins_by_winner[i]["red"]) + " | BLUE: " + str(wins_by_winner[i]["blue"])


		if wins_by_winner[i]["red"] == 2:
			winners[i] = latest_match.get_red_alliance().get_teams()
			losers[i] = latest_match.get_blue_alliance().get_teams()
			overall_winner[i] = "red"
			overall_loser[i] = "blue"
		elif wins_by_winner[i]["blue"] == 2:
			winners[i] = latest_match.get_blue_alliance().get_teams()
			losers[i] = latest_match.get_red_alliance().get_teams()
			overall_winner[i] = "blue"
			overall_loser[i] = "red"
		else:
			print "Elimination Error"

		print "WINNER: " + overall_winner[i] + " | LOSER: " + overall_loser[i]

		if wins_by_winner[i][overall_loser[i]] > 0:
			for loser in losers[i]:
				eliminated.write(str(loser[3:]) + "\n")

	eliminated.close()

	for i in range(section_count[section]):
		f.write(str(i) + ",")
		for j in range(len(winners[i])):
			f.write(winners[i][j] + ",")
			elim_scoring.write(winners[i][j][3:] + "\n")
		for j in range(len(losers[i])):
			f.write(losers[i][j] + ",")
		f.write(str(wins_by_winner[i][overall_winner[i]]) + "-" + str(wins_by_winner[i][overall_loser[i]]) + "-" + str(wins_by_winner[i]["tie"]) + "\n")
	f.close()
	elim_scoring.close()

	if to_slack:
		EventUpdates.elims_section_update(eventid, section, output, roster_file)

# To be run at the end of an event
# Calculates the earned fantasy points of all teams
def final_data_update(eventid, roster_file, to_slack = False):
	fantasy_points = {}
	elim_wins = {}
	
	data = "data/fantasy/" + eventid
	quals_data = open(data +"/qual_data.csv", "r")
	on_alliance_data = open(data + "/on_alliances.txt", "r")
	alliance_captain_data = open(data + "/alliance_captains.txt", "r")
	qf_winners_data = open(data + "/quarterfinals_winners.txt", "r")    
	sf_winners_data = open(data + "/semifinals_winners.txt", "r")  
	f_winners_data = open(data + "/finals_winners.txt", "r")
	qf_eliminated_data = open(data + "/quarterfinalseliminated.txt", "r")    
	sf_eliminated_data = open(data + "/semifinalseliminated.txt", "r")  
	f_eliminated_data = open(data + "/finalseliminated.txt", "r")
	fantasy_point_data = open(data + "/fantasy_point_data.csv", "w")

	with quals_data:
		quals_content = quals_data.read().splitlines()
	for team in quals_content:
		comma1 = team.index(",")
		comma2 = team.index(",", comma1+1)
		fantasy_points[team[:comma1]] = float(team[comma1+1:comma2])

	with on_alliance_data:
		on_alliance_content = on_alliance_data.read().splitlines()
	for team in on_alliance_content:
		fantasy_points[team] += 5
		elim_wins[team] = 0


	with qf_winners_data:
		qf_winners_content = qf_winners_data.read().splitlines()
	for team in qf_winners_content:
		fantasy_points[team] += 10
		elim_wins[team] = 2

	with sf_winners_data:
		sf_winners_content = sf_winners_data.read().splitlines()
	for team in sf_winners_content:
		fantasy_points[team] += 20
		elim_wins[team] = 4

	with f_winners_data:
		f_winners_content = f_winners_data.read().splitlines()
	for team in f_winners_content:
		fantasy_points[team] += 40
		elim_wins[team] = 6


	with qf_eliminated_data:
		qf_eliminated_content = qf_eliminated_data.read().splitlines()
	for team in qf_eliminated_content:
		fantasy_points[team] += 5
		elim_wins[team] = 1

	with sf_eliminated_data:
		sf_eliminated_content = sf_eliminated_data.read().splitlines()
	for team in sf_eliminated_content:
		fantasy_points[team] += 5
		elim_wins[team] = 3

	with f_eliminated_data:
		f_eliminated_content = f_eliminated_data.read().splitlines()
	for team in f_eliminated_content:
		fantasy_points[team] += 5
		elim_wins[team] = 5

	with alliance_captain_data:
		alliance_captain_content = alliance_captain_data.read().splitlines()
	for team in alliance_captain_content:
		fantasy_points[team] += 2 * elim_wins[team]

	sorted_fantasy_points = sorted(fantasy_points.items(), key=operator.itemgetter(1), reverse=True)

	for team in sorted_fantasy_points:
		fantasy_point_data.write(str(team[0]) + "," + str(team[1]) + "\n")

	quals_data.close()
	on_alliance_data.close()
	qf_winners_data.close()
	sf_winners_data.close()
	f_winners_data.close()
	fantasy_point_data.close()

	if to_slack:
		EventUpdates.final_update(eventid, data,roster_file)

mutlipliers = {"Regional" : 1, "District" : 0.5, "District Championship" : 1.5, "District Championship Division" : 0.75, "Championship Division" : 1.5}
def player_points_data_update(eventid, roster_file, to_slack=True):
	rosters = GenerateRosterLists.generate_roster_lists(roster_file)
	fantasy_scores = {}

	event = TBAconnection.get_event(eventid)
	week = event.get_week()
	event_type = event.get_event_type()



	output = "data/fantasy"

	fantasy_point_data = open(output + "/" + eventid + "/fantasy_point_data.csv", "r")    

	with fantasy_point_data:
		content = fantasy_point_data.read().splitlines()
	fantasy_point_data.close()

	for team in content:
		comma_index = team.index(",")
		fantasy_scores[team[:comma_index]] = team[comma_index+1:]

	f = open("data/fantasy/players/week" + str(week) + "/" + eventid + ".csv", "w")

	for roster in rosters:
		for team in roster:
			if team in fantasy_scores:
				score = fantasy_scores[team]
				multiplier = mutlipliers[event_type]
				final_score = float(score) * multiplier
				f.write(roster[0] + "," + team + "," + score + "," + str(multiplier) + "," + str(final_score) + "\n")

	f.close()

	if to_slack:
		EventUpdates.players_points_update(eventid, output, week)
		