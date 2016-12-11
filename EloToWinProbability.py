# Computes the win probability of a matchup based solely on elo rating
# Assumes naive combination of elos

STRENGTH_FACTOR = 133

import scipy as sp
import math
import FullNaiveEloStatistics
import NaiveEloStatistics

def elo_to_win_probability(blue_matrix, red_matrix):
	assert len(blue_matrix) == 3
	assert len(red_matrix) == 3

	blue_transformed = 0
	red_transformed = 0

	for i in range(3):
		blue_transformed += math.pow(10, blue_matrix[i][1] / STRENGTH_FACTOR)
		red_transformed += math.pow(10, red_matrix[i][1] / STRENGTH_FACTOR)

	total = red_transformed + blue_transformed
	red_rate = red_transformed / total
	blue_rate = blue_transformed / total
	if red_rate > blue_rate:
		advantage = "red"
	else:
		advantage = "blue"

	print "Blue Alliance: {:.0f}\t{:.0f}\t{:.0f}".format(blue_matrix[0][0], blue_matrix[1][0], blue_matrix[2][0])
	print "Red Alliance: {:.0f}\t{:.0f}\t{:.0f}".format(red_matrix[0][0], red_matrix[1][0], red_matrix[2][0])
	print "Win probability split is {:.3f} to {:.3f} in favor of {}".format(blue_rate, red_rate, advantage)

indexed_teams, elo = FullNaiveEloStatistics.full_naive_elo_stats("2016casj")
print elo

red_teams = ["114", "1280", "5905"]
blue_teams = ["3256", "5700", "4904"]

blue = sp.empty((3,2))
red = sp.empty((3,2))

for i in range(3):
	blue[i][0] = blue_teams[i]
	blue[i][1] = elo[indexed_teams.index("frc" + blue_teams[i])][1]
	red[i][0] = red_teams[i]
	red[i][1] = elo[indexed_teams.index("frc" + red_teams[i])][1]
elo_to_win_probability(blue, red)