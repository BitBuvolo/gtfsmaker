
import secrets
import shutil
import math

def randhex():
	s = ""
	for i in range(6):
		s += secrets.choice("0123456789ABCDEF")
	return s

stops = {}
lines = {}

routeid = 1
stopid = 1

agency_txt = """agency_name,agency_url,agency_timezone,agency_lang,agency_phone
Your Transit Agency,http://www.yourtransitagency.com,America/New_York,en,22-555-305764
"""

def times():
	stopslist = list(stops.values())
	for i in range(len(stopslist)):
		for j in range(i+1, len(stopslist)):
			lat1 = float(stopslist[i]["lat"])
			lat2 = float(stopslist[j]["lat"])
			lon1 = float(stopslist[i]["lon"])
			lon2 = float(stopslist[j]["lon"])

			deltaLat = abs(lat1 - lat2) * 110.574
			deltaLon = abs(lon1 * 111.320 * math.cos(lat1) - lon2 * 111.320 * math.cos(lat2))

			dist = math.sqrt(deltaLat*deltaLat + deltaLon*deltaLon)

			print(stopslist[i]["name"] + " <-> " + stopslist[j]["name"] + " : " + str(dist / 40) + "h" )

def export():
	f = open("arrange/agency.txt", "w+")
	f.write(agency_txt)
	f.close()

	f = open("arrange/routes.txt", "w+")
	f.write("route_id,route_short_name,route_long_name,route_type,route_color\n")
	for line in lines.values():
		f.write("R" + str(line["id"]) + "," + "L" + str(line["id"]) + "," + line["name"] + ",1," + randhex() + "\n")
	f.close()

	f = open("arrange/stops.txt", "w+")
	f.write("stop_id,stop_name,stop_lat,stop_lon\n")
	for stop in stops.values():
		f.write(stop["id"] + "," + stop["name"] + "," + stop["lon"] + "," + stop["lat"] + "\n")
	f.close()

	f = open("arrange/trips.txt", "w+")
	f.write("route_id,service_id,trip_id\n")
	service_id = 1
	for line in lines.values():
		f.write("R" + line["id"] + "," + str(service_id) + "," + "T" + line["id"] + "\n")
		service_id+=1
	f.close()

	f = open("arrange/stop_times.txt", "w+")
	f.write("trip_id,arrival_time,departure_time,stop_id,stop_sequence\n")
	for line in lines.values():
		count = 1
		for stopname in line["stops"]:
			stop = stops[stopname]
			f.write("T" + line["id"] + ",8:00:00" + ",8:00:00" + "," + stop["id"] + "," + str(count) + "\n")
			count+=1

		"""
		# make 2-way
		for stopname in list(reversed(line["stops"]))[1:]:
			stop = stops[stopname]
			f.write("T" + line["id"] + ",8:00:00" + ",8:00:00" + "," + stop["id"] + "," + str(count) + "\n")
			count+=1
		"""
	f.close()

	shutil.make_archive("arrange", 'zip', "arrange")

	print("successful export!")

def printhelp():
	print("* commands:");
	print("* ns <stopname> <lon> <lat> : add new stop")
	print("* nl <linename> <stop1> <stop2>... : add new line through stops")
	print("* ds <stopname> : delete stop")
	print("* dl <linename> : delete line")
	print("* times : get time distance between every pair of stops")
	print("* exp : export to zip")
	print("* (Note: input correctness is NOT checked!)")

def printstatus():
	print("stops:")
	for name in stops.keys():
		print ("	" + name + " (lon: " + stops[name]["lon"] + " | lat: " + stops[name]["lat"] + ")")

	print("lines:")
	for name in lines.keys():
		print("	" + name + " (" + str(lines[name]["stops"]) + ")")

printhelp()
print(" ")
while True:
	cmd = input("> ");
	toks = cmd.split(" ")

	try:
		if toks[0] == "ns":
			stops[toks[1]] = {"name":toks[1], "id": str(stopid), "lon": toks[2], "lat": toks[3]}
			stopid+=1

		elif toks[0] == "ds":
			del stops[toks[1]]

		elif toks[0] == "nl":
			line_stops = toks[2:]
			lines[toks[1]] = {"name": toks[1], "id": str(routeid), "stops": line_stops}
			routeid+=1;

		elif toks[0] == "dl":
			del lines[toks[1]]
		elif toks[0] == "exp":
			export()
		elif toks[0] == "times":
			times()
		else:
			print("unknown command!")
			printhelp()
	except Exception as e:
		print("something went wrong: ")
		print(e)
		printhelp()
	print(" ")
	printstatus()
	print(" ")




