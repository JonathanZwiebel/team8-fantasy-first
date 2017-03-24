import EventDataUpdates as e
import TeamSheets as t
import GenerateFFRosterData as g

roster_date = "mar21"
roster_file = "data/" + roster_date + "/rosters-" + roster_date + ".csv"


channel = "fantasy-first-bot"
eventid = "2017flwp"

e.initial_data_update(eventid, to_slack=True)
e.quals_data_update(eventid, roster_file, to_slack=True)
e.alliance_selection_data_update(eventid, roster_file, to_slack=True)
e.elims_section_data_update(eventid, "quarterfinals", roster_file, to_slack=True)
e.elims_section_data_update(eventid, "semifinals", roster_file, to_slack=True)
e.elims_section_data_update(eventid, "finals", roster_file, to_slack=True)
e.final_data_update(eventid, roster_file, to_slack=True)
e.player_points_data_update(eventid, roster_file, to_slack=True)

# t.extract_teams_and_events(2017)

# g.generate("data", roster_date)