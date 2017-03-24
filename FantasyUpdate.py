import EventDataUpdates as e

channel = "fantasy-first-bot"

eventid = "2017flwp"
roster_file = "data/mar21/rosters-mar21.csv"

e.initial_data_update(eventid, to_slack=True)
e.quals_data_update(eventid, roster_file, to_slack=True)
e.alliance_selection_data_update(eventid, roster_file, to_slack=True)
e.elims_section_data_update(eventid, "quarterfinals", roster_file, to_slack=True)
e.elims_section_data_update(eventid, "semifinals", roster_file, to_slack=True)
e.elims_section_data_update(eventid, "finals", roster_file, to_slack=True)
e.final_data_update(eventid, roster_file, to_slack=True)
e.player_points_data_update(eventid, roster_file, to_slack=True)