
"""**************************************************************************************************
** ds18b20.py - Getting temperatures from multiple													*
** DS18b20 temperature sensor																		*
*****************************************************************************************************
** Author : Xavier Caron																			*
** Version : 1.0																					*
** based on Adafruit script																		  	*
** https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software *
**																								   	*
** This script checks all ds18b20 sensor plugged to the Raspberry pi							   	*
** and creates a raw csv file formatted as such :												   	*
** DATETIME ; SENSOR1 ; SENSOR2 ; ...															   	*
**																								   	*
** Call with arguments :																		   	*
**																								   	*
** python bchrectemp.py brewID etapeID 															   	*
**																								   	*
** Website : blog.biologeek.io																	   	*
**																								   	*
**																								   	*
*****************************************************************************************************
"""


import os
import glob
import datetime
import time
import sys
from MySQLDB import MySQLDB


# Loading 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

MAIN_DIR = "/opt/tomcat/webapps"
PROJECT_DIR = MAIN_DIR+"/brewspberry-batches"
base_dir = '/sys/bus/w1/devices'
device_folder = glob.glob(base_dir + '/28*')
device_file = [f + '/w1_slave' for f in device_folder]
csv_to_write = PROJECT_DIR+"/fic/ds18b20_raw_measurements.csv"

db_conf_file = PROJECT_DIR+"/conf/db/mysql.conf"
db_table_name = "TemperatureMeasurement"

time_to_sleep = 0.2


# Returns a list of probe UUIDs
probe_uuids = [folder[-15:] for folder in device_folder]





mysql = MySQLDB (db_conf_file)
mysql.connect()
"""
postgres = PostgresDB (db_conf_file)
postgres.connect()
"""

def read_temp_raw():
	"""
		function read_temp_raw
		- IN : void
		- OUT : An array containing the lines of device_file

		This function loops over file lines and returns raw data
	"""
	i=0
	lines = [None]*len(device_file)
	if len (device_file) > 0 :
		# Looping over files list
		for file in device_file :
			f = open(file, 'r')
			lines[i] = f.readlines()
			i+=1
	
		print str(i)+" files read !"
		f.close()
	else :
		print "0 files read"
		
	return lines

def read_temp():
	"""
		function read_temp
		- IN : void
		- OUT : An array containing all probes temperatures in degrees C

		This function loops over read files and searches for temperature values
	"""

	print "Reading files"
	file_lines = read_temp_raw()

	j=0
	temp_c=[None]*len(device_file)
	if len(file_lines) > 0 :

		
		print len(file_lines)
		# While the probe is not ready, it sleeps for a little time and tries back
		while file_lines[0][0].strip()[-3:] != 'YES':	
			time.sleep(time_to_sleep)
			file_lines = read_temp_raw()

		for lines in file_lines :
			# For each line we try to find the temperature value
			equals_pos = lines[1].find('t=')
	
			if equals_pos != -1 :
				print "Getting temperature"
				temp_string = lines[1][equals_pos+2:]
				temp_c[j] = float(temp_string) / 1000.0
			j+=1
		
	return temp_c


def write_temp_into_csv (data,w):
	"""
		function write_temp_into_csv
		- IN : data : String to write 
		- OUT : void
		This function writes data in csv file declared in the header csv_to_write
		If data != \n, it deletes the \n character
	"""


	if (str (data) !="\n") :
		w.write(str(data).rstrip("\n"))
	else :
		if (os.stat(w).st_size != 0):
			w.write (str(data))
	


def write_temp_into_mysql (date, uuid, probe, temperature, brassin, etape, actioner):
	"""
	
		function write_temp_into_mysql
		- IN : date (current date), probe (current probe), temperature (current temperature)
		- OUT : void

		This function inserts a new entry in mysql table for probes (name defined in header)
	"""

	req = "INSERT INTO `"+db_table_name+"` (`tmes_id`, `tmes_date`, `tmes_probeUI`, `tmes_probe_name`, `tmes_value`, `tmes_act_id`, `tmes_etape_id`, `tmes_bra_id`) VALUES (NULL, '"+str(date)+"', '"+str(uuid)+"', 'PROBE"+str(probe)+"', '"+str(temperature)+"', '"+str(actioner)+"', "+str(etape)+", "+str(brassin)+");"
	
	print req
	try:
		mysql.executeQuery (req)
		print " INSERT SUCCEEDED"

	except Exception :
		print "*** INSERT FAILED ****"





print device_folder


while True:
	w = open(csv_to_write, 'a')
	try :
		
		# if len = 4 insert in DB, else not
		if len(sys.argv) != 4 and len(sys.argv) != 1 :
			print "FATAL : Program called with "+str(len(sys.argv))+" arguments"
			print "Please call like that : "
			print ""
			print "python bchrectemp.py brewID etapeID actionerID"
			
			sys.exit(1)
		if len(sys.argv) == 4 :	
			mes_brew = sys.argv[1]
			mes_step = sys.argv[2]
			mes_actioner = sys.argv[3]
			
		else :
			mes_brew = 0
			mes_step = 0
			mes_actioner = 0

		date = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
		temperatures = read_temp()
		print temperatures
		if len(temperatures) > 0 :
			
			write_temp_into_csv("\n",w)
			write_temp_into_csv(date,w)
			write_temp_into_csv(';'+str(mes_brew),w)
			write_temp_into_csv(';'+str(mes_step),w)
			write_temp_into_csv(';'+str(mes_actioner),w)
			print temperatures

			i=0
			for temp in temperatures :

				probeUUID= os.path.basename(device_folder[i])
			
				write_temp_into_csv(';'+str(probe_uuids[i]),w)
				write_temp_into_csv(';'+str(temp),w)
				
				if len(sys.argv) == 4 :
					write_temp_into_mysql(date, probe_uuids[i], str(i), temp, mes_brew, mes_step, mes_actioner)
					print "write_temp_into_mysql(date, probe_uuids[i], str(i), temp, mes_brew, mes_step, mes_actioner)"
				i+=1




			time.sleep(0.5)
		w.close()
	except KeyboardInterrupt:
		print "Bye"
		write_temp_into_csv("\n",w)
		mysql.disconnect()
		sys.exit(0)

