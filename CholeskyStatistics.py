# This class takes an event ID and outputs calculated Chokelsky statistics based on data from thebluealliance.com. Cholesky decomposition retains original triangular matrices so that 
# multiple statistics can be calculated in quick succession. This procedure takes 0.5n^2 + (k + 0.5)n row operations where n is the number of teams at the event and k is the number of statistics to calculate
#
# Currently implemented statistics:
#  - OPR Total Points
#  - High Goals
#  - 
#
# Author: Jonathan Zwiebel
# Version: 28 November 2016

import TBAconnection 
import scipy as sp
from scipy import linalg
import math

# Receieves data from TBA API
eventid = "2016casj"
matches = TBAconnection.get_matches_with_teams(eventid)
teams =  TBAconnection.get_teams_at_event(eventid)

# Creates list to index and store team numbers
indexed_teams = []
for team in teams:
	indexed_teams.append(str(team.get_key()))

# Fills coefficient and resultant vector with zeroes
statistics = ["Total Points", "High Goals", "Auto Points", "Ranking Points", "Breach Achieved", "Defense Crossings", "Tower Damage", "Scale Points", "Winning Margin"]
A = sp.zeros((len(teams),len(teams)),dtype=int)
B = sp.zeros((len(teams),len(statistics)),dtype=int)

# Iterates through each match
for match in matches:
	if match.get_key_as_displayable().isdigit():
		blue_teams = match.get_blue_alliance().get_teams()
		red_teams = match.get_red_alliance().get_teams()
		# Fills the coefficient matrix
		for i in range(3):
			for j in range(3):
				# TODO: Consider taking the log of the L matrix vlaues when calculating OPRs of binary statistics
				A[indexed_teams.index(blue_teams[i])][indexed_teams.index(blue_teams[j])] += 1
				A[indexed_teams.index(red_teams[i])][indexed_teams.index(red_teams[j])] += 1
		# Fills the resultant vector
		for k in range(3):
			B[indexed_teams.index(blue_teams[k])][0] += match.get_blue_total()
			B[indexed_teams.index(red_teams[k])][0] += match.get_red_total()
			B[indexed_teams.index(blue_teams[k])][1] += match.get_blue_teleop_boulders_high()
			B[indexed_teams.index(red_teams[k])][1] += match.get_red_teleop_boulders_high()
			B[indexed_teams.index(blue_teams[k])][2] += match.get_blue_auto_points()
			B[indexed_teams.index(red_teams[k])][2] += match.get_red_auto_points()
			B[indexed_teams.index(blue_teams[k])][3] += match.get_blue_rp()
			B[indexed_teams.index(red_teams[k])][3] += match.get_red_rp()
			B[indexed_teams.index(blue_teams[k])][4] += match.get_blue_breach()
			B[indexed_teams.index(red_teams[k])][4] += match.get_red_breach()
			B[indexed_teams.index(blue_teams[k])][5] += match.get_blue_crossings()
			B[indexed_teams.index(red_teams[k])][5] += match.get_red_crossings()
			B[indexed_teams.index(blue_teams[k])][6] += match.get_blue_tower_damage()
			B[indexed_teams.index(red_teams[k])][6] += match.get_red_tower_damage()
			B[indexed_teams.index(blue_teams[k])][7] += match.get_blue_scale_points()
			B[indexed_teams.index(red_teams[k])][7] += match.get_red_scale_points()
			B[indexed_teams.index(blue_teams[k])][8] += match.get_blue_winning_margin()
			B[indexed_teams.index(red_teams[k])][8] += match.get_red_winning_margin()


# Removes teams that did not play to keep matrix Hermitian
# TODO(Jonathan): Fill the matrix dynamically?
index = 0
while index < len(A):
	if A[index][index] == 0:
		A = sp.delete(A, index, 0)
		A = sp.delete(A, index, 1)
		B = sp.delete(B, index, 0)
		team_to_delete = indexed_teams[index]
		indexed_teams = sp.delete(indexed_teams, index, 0)
	else:
		index += 1

# Cholesky decomposition
# cond = sp.linalg.expm_cond(A)
L = sp.linalg.cholesky(A, lower=True, overwrite_a=True, check_finite=False)
sp.savetxt("Pairings.csv", sp.asarray(L), delimiter=",")


# Forward substitution
Z = sp.linalg.solve_triangular(L, B, lower=True, trans=0, unit_diagonal=False, overwrite_b=True, check_finite=False)


# Backward substitution
Lt = sp.transpose(L)
X = sp.linalg.solve_triangular(Lt, Z, lower=False, trans=0, unit_diagonal=False, overwrite_b=True, check_finite=False)


# Prints results
sp.set_printoptions(threshold=sp.inf,suppress=True)
result = sp.empty(shape=(len(X),len(statistics) + 1))
for i in range(len(X)):
	result[i][0] = int(indexed_teams[i][3:])
	for j in range(1, len(statistics) + 1):
		result[i][j] = float(X[i][j-1])
sortby = "Winning Margin"
result = result[sp.array(result[:,statistics.index(sortby) + 1].argsort(axis=0).tolist()).ravel()]
result = sp.flipud(result)

print "Teams by CCWMs"
print result

sp.savetxt("Results.csv", sp.asarray(result), delimiter=",")

# print "Condition Number: {}".format(cond)
