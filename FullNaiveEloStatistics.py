# This class calculates an elo rating for an individual event
# The current implementation assumes equal team contribution and uses equal team loss / gain
# This setup uses all qualification AND elimination matches
# Current setup uses 1 for wins, 0.5 for ties, 0 for losses

STARTING_ELO = 1500				# FIDE Value
STRENGTH_FACTOR = 133	 		# FIDE Value scaled
ADJUSTMENT_FACTOR = 192			# FIDE Value scaled

import TBAconnection 
import math
import scipy as sp

def full_naive_elo_stats(eventid):
	# Receieves data from TBA API
	matches = TBAconnection.get_matches_with_teams(eventid)
	teams =  TBAconnection.get_teams_at_event(eventid)

	# Creates list to index and store team numbers
	indexed_teams = []
	elo = []
	for team in teams:
		indexed_teams.append(str(team.get_key()))
		elo.append(STARTING_ELO)

	# Note: These matches are not received in correct order, this may cause issues on live data pulls
	for match in matches:
			blue_teams = match.get_blue_alliance().get_teams()
			red_teams = match.get_red_alliance().get_teams()
			blue_transformed = 0
			red_transformed = 0
			for i in range(0,3):
				blue_transformed += math.pow(10, elo[indexed_teams.index(blue_teams[i])] / STRENGTH_FACTOR)
				red_transformed += math.pow(10, elo[indexed_teams.index(red_teams[i])] / STRENGTH_FACTOR)
			total = blue_transformed + red_transformed
			e_red = red_transformed / total
			e_blue = blue_transformed / total
			if match.get_winner() == "blue":
				 s_red = 0
				 s_blue = 1
			elif match.get_winner() == "red":
				s_red = 1
				s_blue = 0
			else:
				s_red = 0.5
				s_blue = 0.5
			adj_red = ADJUSTMENT_FACTOR * (s_red - e_red)
			adj_blue = ADJUSTMENT_FACTOR * (s_blue - e_blue)
			for i in range(0,3):
				elo[indexed_teams.index(red_teams[i])] += adj_red
				elo[indexed_teams.index(blue_teams[i])] += adj_blue


	result = sp.empty(shape=(len(indexed_teams), 2))
	for i in range(len(indexed_teams)):
		result[i][0] = int(indexed_teams[i][3:])
		result[i][1] = elo[i]
	
	sorted_result = result
	sorted_result = sorted_result[sp.array(result[:,1].argsort(axis=0).tolist()).ravel()]
	sorted_result = sp.flipud(sorted_result)
	sp.savetxt("data/elo.csv", sorted_result, delimiter=",")

	return indexed_teams, result