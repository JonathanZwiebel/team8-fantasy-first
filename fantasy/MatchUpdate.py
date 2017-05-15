import TBAconnection as t
import GenerateRosterLists
import Slack
from FormattedTeam import formatted_team

roster_date = "apr5play"
roster_file = "data/" + roster_date + "/rosters-" + roster_date + ".csv"

def get_default_attachement(match_id, attachment_text):
		return [
			{
				"fallback": "Error in sending message",
				"color": "#0000ff",
				"title_link": "https://www.thebluealliance.com/match/" + match_id,
				"mrkdwn_in": ["text"],
				"text": attachment_text,
			}
		]

def match_update(match_id, roster_file, fantasy):
	match = t.get_match(match_id)
	red_points = match.get_red_total()
	blue_points = match.get_blue_total()

	red_teams = match.get_red_alliance().get_teams()
	blue_teams = match.get_blue_alliance().get_teams()

	if red_points > blue_points:
		result = "red"
		winners = red_teams
		losers = blue_teams
		win_pt = red_points
		lose_pt = blue_points
		winner_rotor = match.get_red_rotor_rp()
		winner_kpa = match.get_red_kpa_rp()
		loser_rotor = match.get_blue_rotor_rp()
		loser_kpa = match.get_blue_kpa_rp()
	elif blue_points > red_points:
		result = "blue"
		winners = blue_teams
		losers = red_teams
		win_pt = blue_points
		lose_pt = red_points
		winner_rotor = match.get_blue_rotor_rp()
		winner_kpa = match.get_blue_kpa_rp()
		loser_rotor = match.get_red_rotor_rp()
		loser_kpa = match.get_red_kpa_rp()
	else:
		result = "tie"
		tie_pt = blue_points
		blue_rotor = match.get_blue_rotor_rp()
		blue_kpa = match.get_blue_kpa_rp()
		red_rotor = match.get_red_rotor_rp()
		red_kpa = match.get_red_kpa_rp()

	rosters = GenerateRosterLists.generate_roster_lists(roster_file)

	event_id = match_id.split("_")[0]
	event = t.get_event(event_id)

	attachment_text = event.get_short_name() + " Quals " + match_id.split("_")[1][2:]  + ": " + "thebluealliance.com/match/" + match_id

	if result != "tie":
		attachment_text += "\nWinners: "
		for i in range(3):
			if fantasy:
				attachment_text += formatted_team(str(winners[i][3:]), rosters) + " "
			else:
				attachment_text += str(winners[i][3:]) + " "
		attachment_text += "with " + str(win_pt) + " points"
		if winner_rotor:
			attachment_text += " and 4 rotors"
		if winner_kpa:
			attachment_text += " and 40+ kPa"
		attachment_text += "\nLosers: "
		for i in range(3):
			if fantasy:
				attachment_text += formatted_team(str(losers[i][3:]), rosters) + " "
			else:
				attachment_text += str(losers[i][3:]) + " "
		attachment_text += "with " + str(lose_pt) + " points"
		if loser_rotor:
			attachment_text += " and 4 rotors"
		if loser_kpa:
			attachment_text += " and 40+ kPa"
	else:
		attachment_text += "\Tie: "
		for i in range(3):
			if fantasy:
				attachment_text += formatted_team(str(blue[i][3:]), rosters) + " "
			else:
				attachment_text += str(blue[i][3:]) + " "
		attachment_text += "with " + str(tie_pt) + " points"
		if blue_rotor:
			attachment_text += " and 4 rotors"
		if blue_kpa:
			attachment_text += " and 40+ kPa"
		attachment_text += "\Tie: "
		for i in range(3):
			if fantasy:
				attachment_text += formatted_team(str(red[i][3:]), rosters) + " "
			else:
				attachment_text += str(red[i][3:]) + " "
		attachment_text += "with " + str(tie_pt) + " points"
		if red_rotor:
			attachment_text += " and 4 rotors"
		if red_kpa:
			attachment_text += " and 40+ kPa"

	attachments = get_default_attachement(match_id, attachment_text)

	if fantasy:
		Slack.send_message("", attachments)
	else:
		Slack.send_comp_message("", attachments)