# This class takes an event ID and outputs calculated Chokelsky statistics based on data from thebluealliance.com. Cholesky decomposition retains original triangular matrices so that 
# multiple statistics can be calculated in quick succession. This procedure takes 0.5n^2 + (k + 0.5)n row operations where n is the number of teams at the event and k is the number of statistics to calculate
#
# Currently implemented statistics:
#  - OPR_total_points
#
# Author: Jonathan Zwiebel
# Version: 28 November 2016

import TBAconnection 
import scipy as sp
from scipy import linalg

# Receieves data from TBA API
eventid = "2016casj"
matches = TBAconnection.get_matches_with_teams(eventid)
teams =  TBAconnection.get_teams_at_event(eventid)

# Creates list to index and store team numbers
indexed_teams = []
for team in teams:
	indexed_teams.append(str(team.get_key()))

# Fills coefficient and resultant vector with zeroes
A = sp.zeros((len(teams),len(teams)),dtype=int)
b_points = sp.zeros((len(teams),1),dtype=int)
b_tele_high = sp.zeros((len(teams),1),dtype=int)

# Iterates through each match
for match in matches:
	if match.get_key_as_displayable().isdigit():
		blue_teams = match.get_blue_alliance().get_teams()
		red_teams = match.get_red_alliance().get_teams()
		# Fills the coefficient matrix
		for i in range(3):
			for j in range(3):
				A[indexed_teams.index(blue_teams[i])][indexed_teams.index(blue_teams[j])] += 1
				A[indexed_teams.index(red_teams[i])][indexed_teams.index(red_teams[j])] += 1
		# Fills the resultant vector
		for k in range(3):
			b_points[indexed_teams.index(blue_teams[k])] += match.get_blue_total()
			b_points[indexed_teams.index(red_teams[k])] += match.get_red_total()
			b_tele_high[indexed_teams.index(blue_teams[k])] += match.get_blue_teleop_boulders_high()
			b_tele_high[indexed_teams.index(red_teams[k])] += match.get_red_teleop_boulders_high()


# Removes teams that did not play to keep matrix Hermitian
# TODO(Jonathan): Fill the matrix dynamically?
index = 0
while index < len(A):
	if A[index][index] == 0:
		A = sp.delete(A, index, 0)
		A = sp.delete(A, index, 1)
		b_points = sp.delete(b_points, index, 0)
		b_tele_high = sp.delete(b_tele_high, index, 0)
		team_to_delete = indexed_teams[index]
		indexed_teams = sp.delete(indexed_teams, index, 0)
	else:
		index += 1

# Cholesky decomposition
L = sp.linalg.cholesky(A, lower=True, overwrite_a=True, check_finite=False)

# Forward substitution
z_points = sp.linalg.solve_triangular(L, b_points, lower=True, trans=0, unit_diagonal=False, overwrite_b=True, check_finite=False)
z_tele_high = sp.linalg.solve_triangular(L, b_tele_high, lower=True, trans=0, unit_diagonal=False, overwrite_b=True, check_finite=False)

# Backward substitution
Lt = sp.transpose(L)
x_points = sp.linalg.solve_triangular(Lt, z_points, lower=False, trans=0, unit_diagonal=False, overwrite_b=True, check_finite=False)
x_tele_high = sp.linalg.solve_triangular(Lt, z_tele_high, lower=False, trans=0, unit_diagonal=False, overwrite_b=True, check_finite=False)

# Prints results
sp.set_printoptions(threshold=sp.inf,suppress=True)
result = sp.empty(shape=(len(x_tele_high),2))
for i in range(len(x_tele_high)):
	result[i][0] = int(indexed_teams[i][3:])
	result[i][1] = float(x_tele_high[i])
result = result[sp.array(result[:,1].argsort(axis=0).tolist()).ravel()]
result = sp.flipud(result)

print "Teams by Teleop High Goals"
print result

