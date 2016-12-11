# This class uses high and low goal OPRs to determine if a robot was a high goal robot or a low goal robot. It then compares statistics between high and low
# goal robots.
#  
#
# Author: Jonathan Zwiebel
# Version: 4 December 2016

import TBAconnection 
import scipy as sp
from scipy import linalg
import math

# Receieves data from TBA API
eventid = "2016cur"
matches = TBAconnection.get_matches_with_teams(eventid)
teams =  TBAconnection.get_teams_at_event(eventid)

# Creates list to index and store team numbers
indexed_teams = []
for team in teams:
	indexed_teams.append(str(team.get_key()))

# Fills coefficient and resultant vector with zeroes
statistics = ["High Goals", "Low Goals"]
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
			B[indexed_teams.index(blue_teams[k])][0] += match.get_blue_high()
			B[indexed_teams.index(red_teams[k])][0] += match.get_red_high()
			B[indexed_teams.index(blue_teams[k])][1] += match.get_blue_low()
			B[indexed_teams.index(red_teams[k])][1] += match.get_red_low()

# Removes teams that did not play to keep matrix Hermitian
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
sortby = "High Goals"
result = result[sp.array(result[:,statistics.index(sortby) + 1].argsort(axis=0).tolist()).ravel()]
result = sp.flipud(result)

print "Teams by OPR of total high goals"
print result

sp.savetxt("LowHighResults.csv", sp.asarray(result), delimiter=",")

# print "Condition Number: {}".format(cond)
