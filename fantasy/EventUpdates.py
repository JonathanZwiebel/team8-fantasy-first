# This class will handle converting Fantasy data into a format that can be relayed to Slack
# Author: Jonathan Zwiebel
# Version: 1 January 2017

import Slack
from FormattedTeam import formatted_team
from FormattedTeam import on_roster
import GenerateRosterLists

def get_default_attachement(eventid, attachment_text):
		return [
			{
				"fallback": "Error in sending message",
				"color": "#0000ff",
				"title_link": "https://www.thebluealliance.com/event/" + eventid,
				"mrkdwn_in": ["text"],
				"text": attachment_text,
			}
		]


def initial_update(eventid):
	 message = "Tracking started for " + eventid
	 Slack.send_message(message, attach="")

def quals_update(eventid, data, roster_file, highest_score, highest_wm):
	rosters = GenerateRosterLists.generate_roster_lists(roster_file)

	attachment_text = ""

	quals_data = open(data + "/qual_data.csv", "r")    
	with quals_data:
		content = quals_data.read().splitlines()
	quals_data.close()

	info_data = open(data +"/information.txt", "r")
	with info_data:
		event_name = info_data.read().splitlines()[0]
	info_data.close()

	for i in range(len(content)):
		split_content = content[i].split(',')

		number = split_content[0]
		fantasy_points = split_content[1]
		rp = split_content[3]
		record = split_content[4]
		record_bonus = split_content[5]
		high_score = split_content[7] == "True"
		winning_margin = split_content[6] == "True"

		if(on_roster(str(number), rosters)):
			attachment_text += "Team " + formatted_team(str(number), rosters)
			attachment_text += " scores *" + str(fantasy_points) + "* fantasy points"
			attachment_text += " with " + str(rp) + " RP"
			attachment_text += " going "
			if record_bonus == "big":
				attachment_text += "an *undefeated* "
			if record_bonus == "small":
				attachment_text += "an impressive "
			attachment_text += str(record)
			attachment_text += " and ends up ranked in the #" + str(i + 1) + " spot"
			if high_score and not winning_margin:
				attachment_text += " with the high score of " + str(highest_score)
			elif winning_margin and not high_score:
				attachment_text += " with the highest winning margin of " + str(highest_wm)
			elif winning_margin and high_score:
				attachment_text += " with both the high score of " + str(highest_score) + " and highest winning margin of " + str(highest_wm) + "!"
			attachment_text += "\n"

	print attachment_text
	attachments = get_default_attachement(eventid, attachment_text)

	message = "Qualification results are out at the *" + event_name+ "*! - thebluealliance.com/event/" + eventid

	Slack.send_message(message, attachments)



def alliance_selection_update(eventid, data, roster_file):
	rosters = GenerateRosterLists.generate_roster_lists(roster_file)
	attachment_text = ""

	print(data + "/alliance_selection_data.csv")
	alliance_selection_data = open(data + "/alliance_selection_data.csv", "r")    
	with alliance_selection_data:
		content = alliance_selection_data.read().splitlines()
	alliance_selection_data.close()

	info_data = open(data +"/information.txt", "r")
	with info_data:
		event_name = info_data.read().splitlines()[0]
	info_data.close()

	for alliance in content:
		alliance_members = alliance.split(",") # 0 is alliance rank

		attachment_text += "*Alliance " + alliance_members[0] + "*"
		for i in range(1, len(alliance_members)):
			attachment_text += "  |  " + formatted_team(alliance_members[i][3:], rosters)
		attachment_text += "\n"

	print attachment_text
	attachments = get_default_attachement(eventid, attachment_text)

	message = "Alliance selection is complete at the *" + event_name+ "*! - thebluealliance.com/event/" + eventid
	message += " Alliances are listed in pick order with Alliance Captain first."
	Slack.send_message(message, attachments)

def elims_section_update(eventid, section, data, roster_file, expanded_alliances=False):
	rosters = GenerateRosterLists.generate_roster_lists(roster_file)
	attachment_text = ""

	elims_section_data = open(data + "/" + section + "_data.csv")    
	with elims_section_data:
		content = elims_section_data.read().splitlines()
	elims_section_data.close()

	info_data = open(data +"/information.txt", "r")
	with info_data:
		event_name = info_data.read().splitlines()[0]
	info_data.close()

	
	# TODO: Find some library that can process csv files
	for match in content:
		commas = [match.index(",")]
		last_index = commas[0]
		while match.find(",", last_index + 1) != -1:
			last_index = match.index(",", last_index + 1)
			commas.append(last_index)

		if expanded_alliances:
			spacer = 4
		else:
			spacer = 3

		for i in range(1, 1 + spacer):
			attachment_text += formatted_team(str(match[commas[i-1]+1:commas[i]][3:]), rosters) + "  "
		attachment_text += "beat  "
		for i in range(1 + spacer, 1 + 2*spacer):
			attachment_text += formatted_team(str(match[commas[i-1]+1:commas[i]][3:]), rosters) + "  "
		attachment_text += "in a " + match[commas[spacer*2]+1:] + " series"
		attachment_text += "\n"

	print attachment_text

	attachments = get_default_attachement(eventid, attachment_text)

	message = "Results are out for *" + section + "* at the *" + event_name+ "*! - thebluealliance.com/event/" + eventid
	Slack.send_message(message, attachments)

def final_update(eventid, data, roster_file):
	rosters = GenerateRosterLists.generate_roster_lists(roster_file)
	attachment_text = ""

	fantasy_point_data = open(data + "/fantasy_point_data.csv")    
	with fantasy_point_data:
		content = fantasy_point_data.read().splitlines()
	fantasy_point_data.close()

	info_data = open(data +"/information.txt", "r")
	with info_data:
		event_name = info_data.read().splitlines()[0]
	info_data.close()

	for team in content:
		comma_index = team.index(",")
		if(on_roster(team[:comma_index], rosters)):
			attachment_text += "Team " + formatted_team(team[:comma_index], rosters)
			attachment_text += " scored " + team[comma_index+1:] + " fantasy points\n"

	print attachment_text

	attachments = get_default_attachement(eventid, attachment_text)

	message = "We're all wrapped up at the *" + event_name+ "*! - thebluealliance.com/event/" + eventid
	Slack.send_message(message, attachments)

def players_points_update(eventid, data, week):
	f = open(data + "/players/week" + str(week) + "/" + eventid + ".csv")
	with f:
		content = f.read().splitlines()

	info_data = open(data + "/" + eventid +"/information.txt", "r")
	with info_data:
		event_name = info_data.read().splitlines()[0]
	info_data.close()

	attachment_text = ""

	for player_data in content:
		comma1 = player_data.index(",")
		comma2 = player_data.index(",", comma1 + 1)
		comma3 = player_data.index(",", comma2 + 1)
		comma4 = player_data.index(",", comma3 + 1)
		
		player = player_data[:comma1]
		team = player_data[comma1+1:comma2]
		score = player_data[comma2+1:comma3]
		multiplier = player_data[comma3+1:comma4]
		final_score = player_data[comma4+1:]

		attachment_text += "*" + player + "'s " + team + " has scored " + score + " x " + multiplier + " = " + final_score + " fantasy points!*\n"

	print attachment_text

	attachments = get_default_attachement(eventid, attachment_text)

	message = "*Final Fantasy Point Scores for " + event_name + "*"
	Slack.send_message(message, attachments, icon=":deankamen:")