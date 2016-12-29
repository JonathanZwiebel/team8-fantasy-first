# This class scores events based on the performance of their teams
#
# Author: Jonathan Zwiebel
# Version: 28 December 2016

# Scores an event by the arithmetic average of the top 8 teams attending by an input metric
import os

# TODO: Generalize decay coefficients to more than (8, 0.8)
decaying_coefficients = [24.032, 19.226, 15.380, 12.304, 9.844, 7.875, 6.300, 5.039]

def score_linear_average_top(teams_filename, metric, depth=8):
	first = True
	list_of_metrics = []
	with open(teams_filename) as f:
		content = f.read().splitlines()
	for index in range(1, len(content)):
		team = int(content[index])
		if team in metric:
			list_of_metrics.append(metric[team])
	list_of_metrics.sort(reverse=True)
	strength = 0
	for i in range(depth):
		strength += list_of_metrics[i] * decaying_coefficients[i]
	print content[0] + ": " + str(strength)
	return content[0], strength

def load_metric_file(metric_filename):
	metric_dict = {}
	with open(metric_filename) as f:
		content = f.read().splitlines()
	for index in range(len(content)): 
		comma_index = content[index].index(',')
		team = int(content[index][:comma_index])
		metric = float(content[index][comma_index+1:])
		metric_dict[team] = metric
	return metric_dict

metric = load_metric_file("data/sykes_elo.csv")

output_file = open("data/event_strengths_jz1.csv", "w")

start = "data/teamlists/Regional"
for file in os.listdir(start):
	name, strength = score_linear_average_top(start + "/" + file, metric)
	output_file.write(name + "," + str(strength) + "\n")

start = "data/teamlists/District"
for file in os.listdir(start):
	name, strength = score_linear_average_top(start + "/" + file, metric)
	output_file.write(name + "," + str(strength) + "\n")

output_file.close()