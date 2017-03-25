import EventDataUpdates as e
import TeamSheets as t
import GenerateFFRosterData as g
import GenerateFantasyScoreSheet as f

roster_date = "feb28play"
roster_file = "data/" + roster_date + "/rosters-" + roster_date + ".csv"

channel = "fantasy-first"
eventid = "2017mndu2"

e.initial_data_update(eventid, to_slack=False)
e.quals_data_update(eventid, roster_file, to_slack=False)
e.alliance_selection_data_update(eventid, roster_file, to_slack=False)
e.elims_section_data_update(eventid, "quarterfinals", roster_file, to_slack=False)
e.elims_section_data_update(eventid, "semifinals", roster_file, to_slack=False)
e.elims_section_data_update(eventid, "finals", roster_file, to_slack=False)
e.final_data_update(eventid, roster_file, to_slack=True)
e.player_points_data_update(eventid, roster_file, to_slack=False)

# t.extract_teams_and_events(2017)

# g.generate("data", roster_date)

f.generate_fantasy_score_sheet(roster_file, roster_date, 1, "data/feb28play/scores.csv")