from TBAconnection import *
from subprocess import call

matches = get_matches_with_teams("2016cacc")

f = open("out.csv", "w")

for match in matches:
	data = []

	if match.get_key_as_displayable().isdigit():
		data.append([match.get_key_as_displayable(),match.get_blue_alliance().as_string(),match.get_red_alliance().as_string()])

	new = sorted(data, key=lambda i:int(i[0]))

	for lines in new:
		f.write(",".join(lines) + "\n")

f.close()

f = open("out.csv", "r")

data = f.readlines()
data.sort(key=lambda i: int(i.split(",")[0]))
f.close()
with open("realout.csv", "w") as f:
	for line in data:
		for team in line.split(",")[1].split(" "):
                    f.write(team[3:] + "," + line.split(",")[0] + ", BLUE \n" )
		for team in line.split(",")[2].split(" "):
                    f.write(team.replace("\n","")[3:] + "," + line.split(",")[0] + ", RED \n")

call(["rm", "out.csv"])
