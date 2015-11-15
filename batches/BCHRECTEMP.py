#!/usr/bin/env python

"""***************************************************************************************************
** ds18b20.py - Getting temperatures from multiple                                                   *
** DS18b20 temperature sensor                                                                        *
******************************************************************************************************
** Author : Xavier Caron                                                                             *
** based on Adafruit script                                                                          *
** https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software  *
**                                                                                                   *
** This script checks all ds18b20 sensor plugged to the Raspberry pi                                 *
** and creates a raw csv file formatted as such :                                                    *
** DATETIME ; SENSOR1 ; SENSOR2 ; ...                                                                *
**                                                                                                   *
**                                                                                                   *
** Website : blog.biologeek.io                                                                       *
**                                                                                                   *
***************************************************************************************************"""


import os
import glob
import datetime
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')
device_file = [f + '/w1_slave' for f in device_folder]
csv_to_write = "/home/pi/ds18b20_raw_measurements.csv"


def read_temp_raw():
    i=0
    lines = [None]*len(device_file)

    # Looping over files list
    for file in device_file :
        f = open(file, 'r')
        lines[i] = f.readlines()
        i+=1
    
    print str(i)+" files read !"
    f.close()
    return lines

def read_temp():
    print "Reading files"
    file_lines = read_temp_raw()

    j=0

    temp_c=[None]*len(device_file)

    while file_lines[0][0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        file_lines = read_temp_raw()

    for lines in file_lines :
        equals_pos = lines[1].find('t=')

        if equals_pos != -1:
            print "Getting temperature"
            temp_string = lines[1][equals_pos+2:]
            temp_c[j] = float(temp_string) / 1000.0
        j+=1
    return temp_c


def write_temp_into_csv (data):
    w = open(csv_to_write, 'a')
    if (str (data) !="\n") :
        w.write(str(data).rstrip("\n"))
    else :
        w.write (str(data))
    w.close()

print device_folder

while True:
    date = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    temperatures = read_temp()
    print temperatures
    write_temp_into_csv(date)
    print temperatures
    for temp in temperatures :
       write_temp_into_csv(';'+str(temp))
    write_temp_into_csv("\n")

    time.sleep(1)

