# This function is to be used with the fantasy league to format a team according to correct ownership
# If a team is owned by a player, the player name is returned after the team
# If a team is not owned by any player, it is simply returned 

# team is the team number as a string
# rosters is a list of each player's roster where the list contains team name followed by team
def formatted_team(team, rosters):
	for roster in rosters:
		for roster_team in roster:
			if team == roster_team:
				return "_*" + team + " (" + roster[0] + ")*_"
	return team