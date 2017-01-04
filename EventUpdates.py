# This class will handle converting Fantasy data into a format that can be relayed to Slack
# Author: Jonathan Zwiebel
# Version: 1 January 2017

import Slack
from FormattedTeam import formatted_team

def initial_update(eventid):
	 message = "Tracking started for " + eventid
	 Slack.send_message(message, attach="")

def quals_update(eventid, data):
	# TODO: Include rosters in data
	rosters = []
	rosters.append(["MemeTeam", "8"])
	rosters.append(["DreamTeam", "254", "330"])
	rosters.append(["CleanTeam", "118", "971"])

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
		comma1 = content[i].index(",")
		comma2 = content[i].index(",", comma1 + 1)
		comma3 = content[i].index(",", comma2 + 1)

		number = content[i][:comma1]
		fantasy_points = content[i][comma1+1:comma2]
		rp = content[i][comma2+1:comma3]
		record = content[i][comma3+1:]

		attachment_text += str(i + 1) + ". "
		attachment_text += "Team " + formatted_team(str(number), rosters)
		attachment_text += " scores " + str(fantasy_points) + " fantasy points"
		attachment_text += " with " + str(rp) + " RP"
		attachment_text += " going " + str(record)
		attachment_text += "\n"

	attachments = [
		{
			"fallback": "Error in sending message",
			"color": "#0000ff",
			"title_link": "https://www.thebluealliance.com/event/" + eventid,
			"mrkdwn_in": ["text"],
			"text": attachment_text,
		}
	]

	message = "Qualification results are out at the *" + event_name+ "*!"
	message += "\nCheck thebluealliance.com/event/" + eventid + " for updates."

	Slack.send_message(message, attachments)



def alliance_selection_update(eventid, data):
	rosters = []
	rosters.append(["MemeTeam", "8"])
	rosters.append(["DreamTeam", "254", "330"])
	rosters.append(["CleanTeam", "118", "971"])

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

	# TODO: Find some library that can process csv files
	for alliance in content:
		commas = [alliance.index(",")]
		last_index = commas[0]
		while alliance.find(",", last_index + 1) != -1:
			last_index = alliance.index(",", last_index + 1)
			commas.append(last_index)
		commas.append(len(alliance))

		attachment_text += "*Alliance " + alliance[:commas[0]] + "*"
		for i in range(1, len(commas)):
			attachment_text += "  |  " + formatted_team(str(alliance[commas[i-1]+1:commas[i]][3:]), rosters)
		attachment_text += "\n"

	attachments = [
		{
			"fallback": "Error in sending message.",
			"color": "#0000ff",
			"title_link": "https://www.thebluealliance.com/event/" + eventid,
			"mrkdwn_in": ["text"],
			"text": attachment_text,
		}
	]

	message = "Alliance selection is complete at the *" + event_name+ "*!"
	message += " Alliances are listed in pick order with Alliance Captain first."
	message += "\nCheck thebluealliance.com/event/" + eventid + " for updates."
	Slack.send_message(message, attachments)

def elims_section_update(eventid, section, data):
	rosters = []
	rosters.append(["MemeTeam", "8"])
	rosters.append(["DreamTeam", "254", "330"])
	rosters.append(["CleanTeam", "118", "971"])

	attachment_text = ""

	elims_section_data = open(data + "/" + section + "_data.csv")    
	with elims_section_data:
		content = elims_section_data.read().splitlines()
	elims_section_data.close()
	print content

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

		for i in range(1, 4):
			attachment_text += formatted_team(str(match[commas[i-1]+1:commas[i]][3:]), rosters) + "  "
		attachment_text += "beat  "
		for i in range(4, 7):
			attachment_text += formatted_team(str(match[commas[i-1]+1:commas[i]][3:]), rosters) + "  "
		print match[commas[6]+1:]
		if match[commas[6]+1:] == "True":
			attachment_text += "in a 2-1 series"
		else:
			attachment_text += "in a 2-0 series"
		attachment_text += "\n"

	print attachment_text


	attachments = [
		{
			"fallback": "Error in sending message.",
			"color": "#0000ff",
			"title_link": "https://www.thebluealliance.com/event/" + eventid,
			"mrkdwn_in": ["text"],
			"text": attachment_text,
		}
	]

	message = "Results are out for *" + section + "* at the *" + event_name+ "*!"
	message += "\nCheck thebluealliance.com/event/" + eventid + " for updates."
	Slack.send_message(message, attachments)

def final_update(eventid, data):
	rosters = []
	rosters.append(["MemeTeam", "8"])
	rosters.append(["DreamTeam", "254", "330"])
	rosters.append(["CleanTeam", "118", "971"])

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
		attachment_text += "Team " + formatted_team(team[:comma_index], rosters)
		attachment_text += " scored " + team[comma_index+1:] + " fantasy points\n"

	print attachment_text


	attachments = [
		{
			"fallback": "Error in sending message.",
			"color": "#0000ff",
			"title_link": "https://www.thebluealliance.com/event/" + eventid,
			"mrkdwn_in": ["text"],
			"text": attachment_text,
		}
	]

	message = "We're all wrapped up at the *" + event_name+ "*!"
	message += "\nCheck thebluealliance.com/event/" + eventid + " for final results."
	Slack.send_message(message, attachments)

def players_points_update(eventid, data, week):
	f = open(data + "/players/week" + str(week) + "/" + eventid + ".csv")
	with f:
		content = f.read().splitlines()
	print content

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


	attachments = [
		{
			"fallback": "Error in sending message.",
			"color": "#00ff00",
			"title_link": "https://www.thebluealliance.com/event/" + eventid,
			"mrkdwn_in": ["text"],
			"text": attachment_text,
		}
	]

	message = "*Final Fantasy Point Scores for " + event_name + "*"
	Slack.send_message(message, attachments, icon=":deankamen:")