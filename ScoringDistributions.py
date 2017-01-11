# This class gets data from all regional qualification matches and generates csvs with distributions of what
# value was scored for certain game elements
#
# Version: 6 January 2017
# Author: Jonathan Zwiebel

import TBAconnection

def get_2016_data():
	events = TBAconnection.get_event_list(2016)

	points = {}
	winning_margins = {}
	tele_points = {}
	auto_points = {}
	tele_high = {}
	auto_high = {}
	tele_low = {}
	crosses = {}
	scales = {}
	end_tower_strength = {}

	for event in events:
		if event.get_event_type() == "Regional":
			print "Working on " + event.get_key()
			matches = TBAconnection.get_matches_with_teams(event.get_key())
			for match in matches:
				if match.get_good():
					red_score = match.get_red_total()
					red_teleop = match.get_red_teleop_points()
					red_auto = match.get_red_auto_points()
					red_high_tele = match.get_red_teleop_boulders_high()
					red_low_tele = match.get_red_teleop_boulders_low()
					red_high_auto = match.get_red_auto_boulders_high()
					red_crossings = match.get_red_crossings()
					red_scales = match.get_red_scale_points()
					red_end_strength = match.get_red_tower_strength()

					blue_score = match.get_blue_total()
					blue_teleop = match.get_blue_teleop_points()
					blue_auto = match.get_blue_auto_points()
					blue_high_tele = match.get_blue_teleop_boulders_high()
					blue_low_tele = match.get_blue_teleop_boulders_low()
					blue_high_auto = match.get_blue_auto_boulders_high()
					blue_crossings = match.get_blue_crossings()
					blue_scales = match.get_blue_scale_points()
					blue_end_strength = match.get_blue_tower_strength()

					if red_score > blue_score:
						winning_margin = red_score - blue_score
					else:
						winning_margin = blue_score - red_score

					if red_score in points:
						points[red_score] += 1
					else:
						points[red_score] = 1

					if red_teleop in tele_points:
						tele_points[red_teleop] += 1
					else:
						tele_points[red_teleop] = 1

					if red_auto in auto_points:
						auto_points[red_auto] += 1
					else:
						auto_points[red_auto] = 1

					if red_high_tele in tele_high:
						tele_high[red_high_tele] += 1
					else:
						tele_high[red_high_tele] = 1

					if red_low_tele in tele_low:
						tele_low[red_low_tele] += 1
					else:
						tele_low[red_low_tele] = 1

					if red_high_auto in auto_high:
						auto_high[red_high_auto] += 1
					else:
						auto_high[red_high_auto] = 1

					if red_crossings in crosses:
						crosses[red_crossings] += 1
					else:
						crosses[red_crossings] = 1

					if red_scales in scales:
						scales[red_scales] += 1
					else:
						scales[red_scales] = 1

					if red_end_strength in end_tower_strength:
						end_tower_strength[red_end_strength] += 1
					else:
						end_tower_strength[red_end_strength] = 1

					if blue_score in points:
						points[blue_score] += 1
					else:
						points[blue_score] = 1

					if blue_teleop in tele_points:
						tele_points[blue_teleop] += 1
					else:
						tele_points[blue_teleop] = 1

					if blue_auto in auto_points:
						auto_points[blue_auto] += 1
					else:
						auto_points[blue_auto] = 1

					if blue_high_tele in tele_high:
						tele_high[blue_high_tele] += 1
					else:
						tele_high[blue_high_tele] = 1

					if blue_low_tele in tele_low:
						tele_low[blue_low_tele] += 1
					else:
						tele_low[blue_low_tele] = 1

					if blue_high_auto in auto_high:
						auto_high[blue_high_auto] += 1
					else:
						auto_high[blue_high_auto] = 1

					if blue_crossings in crosses:
						crosses[blue_crossings] += 1
					else:
						crosses[blue_crossings] = 1

					if blue_scales in scales:
						scales[blue_scales] += 1
					else:
						scales[blue_scales] = 1

					if blue_end_strength in end_tower_strength:
						end_tower_strength[blue_end_strength] += 1
					else:
						end_tower_strength[blue_end_strength] = 1

					if winning_margin in winning_margins:
						winning_margins[winning_margin] += 1
					else:
						winning_margins[winning_margin] = 1

	print points 
	print winning_margins 
	print tele_points 
	print auto_points 
	print tele_high
	print auto_high 
	print tele_low 
	print crosses 
	print scales 
	print end_tower_strength 

	points_sorted = sorted(points) 
	winning_margins_sorted = sorted(winning_margins) 
	tele_points_sorted = sorted(tele_points) 
	auto_points_sorted = sorted(auto_points) 
	tele_high_sorted = sorted(tele_high) 
	auto_high_sorted = sorted(auto_high) 
	tele_low_sorted = sorted(tele_low) 
	crosses_sorted = sorted(crosses) 
	scales_sorted = sorted(scales) 
	end_tower_strength_sorted = sorted(end_tower_strength) 

	output = "data/2016regionalstats/"
	f_points = open(output + "points.csv", "w")
	f_winning_margins = open(output + "winning_margins.csv", "w")
	f_tele_points = open(output + "tele_points.csv", "w")
	f_auto_points = open(output + "auto_points.csv", "w")
	f_tele_high = open(output + "tele_high.csv", "w")
	f_auto_high = open(output + "auto_high.csv", "w")
	f_tele_low = open(output + "tele_low.csv", "w")
	f_crosses = open(output + "crosses.csv", "w")
	f_scales = open(output + "scales.csv", "w")
	f_end_tower_strength = open(output + "end_strength.csv", "w")

	for key in points_sorted:
		f_points.write(str(key) + "," + str(points[key]) + "\n")
	for key in winning_margins_sorted:
		f_winning_margins.write(str(key) + "," + str(winning_margins[key]) + "\n")
	for key in tele_points_sorted:
		f_tele_points.write(str(key) + "," + str(tele_points[key]) + "\n")
	for key in auto_points_sorted:
		f_auto_points.write(str(key) + "," + str(auto_points[key]) + "\n")
	for key in tele_high_sorted:
		f_tele_high.write(str(key) + "," + str(tele_high[key]) + "\n")
	for key in auto_high_sorted:
		f_auto_high.write(str(key) + "," + str(auto_high[key]) + "\n")
	for key in tele_low_sorted:
		f_tele_low.write(str(key) + "," + str(tele_low[key]) + "\n")
	for key in crosses_sorted:
		f_crosses.write(str(key) + "," + str(crosses[key]) + "\n")
	for key in scales_sorted:
		f_scales.write(str(key) + "," + str(scales[key]) + "\n")
	for key in end_tower_strength_sorted:
		f_end_tower_strength.write(str(key) + "," + str(end_tower_strength[key]) + "\n")
		 	
	f_points.close()
	f_winning_margins.close()
	f_tele_points.close()
	f_auto_points.close()
	f_tele_high.close()
	f_auto_high.close()
	f_tele_low.close()
	f_crosses.close()
	f_scales.close()
	f_end_tower_strength.close()

get_2016_data()