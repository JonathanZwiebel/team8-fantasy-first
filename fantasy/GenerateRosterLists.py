# A method to convert a CSV of roster data into a list of lists

def generate_roster_lists(filename):
	f = open(filename, "r")
	content = f.read().splitlines()

	result = []
	for team in content:
		team_roster = []
		comma_index = team.index(',')
		team_roster.append(team[:comma_index])

		test_split = team.split(',')
		result.append(test_split)
	return result
