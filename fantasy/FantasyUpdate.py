import EventDataUpdates as e
import TeamSheets as t
import GenerateFFRosterData as g
import GenerateFantasyScoreSheet as f
import MatchUpdate as m
import time

roster_date = "apr25play"
roster_file = "data/" + roster_date + "/rosters-" + roster_date + ".csv"

channel = "fantasy-first"

events = ["2017arc", "2017cars", "2017cur", "2017dal", "2017dar", "2017tes"]


for eventid in events:
	e.initial_data_update(eventid, to_slack=False)
	e.quals_data_update(eventid, roster_file, to_slack=False)
	e.alliance_selection_data_update(eventid, roster_file, to_slack=False)
	e.elims_section_data_update(eventid, "quarterfinals", roster_file, to_slack=False, expanded_alliances=True)
	e.elims_section_data_update(eventid, "semifinals", roster_file, to_slack=False, expanded_alliances=True)
	e.elims_section_data_update(eventid, "finals", roster_file, to_slack=True, expanded_alliances=True)
	e.final_data_update(eventid, roster_file, to_slack=True)
	time.sleep(8)


# t.extract_teams_and_events(2017)

# g.generate("data", roster_date)

f.generate_fantasy_score_sheet(roster_file, roster_date, 9, "data/apr25play/scores.csv")

"""
fantasy = True
event = "arc"
match = "104"

match_id = "2017" + event + "_qm" + match
m.match_update(match_id, roster_file, fantasy)
"""