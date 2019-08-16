# Delta distance / speed in meter for 1 h * effect then sum from start to stop

import csv
import math
import enum 
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create key values for table
speed_dict = { 5:0, 10:1, 15:2, 20:3, 25:4, 30:5, 35:6, 40:7, 45:8, 50:9, 55:10, 60:11, 65:12, 70:13, 75:14, 80:15, 85:16, 90:17, 95:18, 100:19, 105:20, 110:21, 115:22, 120:23, 125:24, 130:25} 

degrees_dict = { -45:0, -40:1, -35:2, -30:3, -25:4, -20:5, -15:6, -10:7, -5:8, 0:9, 5:10, 10:11, 15:12, 20:13, 25:14, 30:15, 35:16, 40:17, 45:18 }

# Create table power_table[speed][degrees]
columns, rows = len(speed_dict), len(degrees_dict)
power_table = [[0 for x in range(columns)] for y in range(rows)]

# Variables
line_count = -1

# Get table values
with open('power_table.csv') as csv_table:
    csv_reader = csv.reader(csv_table, delimiter=';')

    for row in csv_reader:
        if line_count == -1:
            line_count += 1
        else:
            for i in range(columns+1):
                if i > 0:
                    power_table[line_count][i - 1] = float(row[i])
            
            # Increment line count
            line_count += 1



# Get inputs
start = int(input("Type start in meter: "))
stop = int(input("Type stop in meter: "))
speed = int(input("Type in speed in kmh: "))

# Reset line count
line_count = 0
power_counter = 0
power_sum = 0
energy_sum = 0

# Read file
with open('wsc_elevation_solbritt_2015.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        elif line_count == 1:
            # Convert all items to floats  
            row = [x.replace(',','.') for x in row]         
            row = [float(x) for x in row]

            # Get elevation and distance
            last_elevation = row[0]
            last_distance = row[1]

            # Increment line count
            line_count += 1
        else:
            
            if row[2] == '':
                continue

            # Convert all items to floats    
            row = [x.replace(',','.') for x in row]          
            row = [float(x) for x in row]

            # Get elevation and distance
            elevation = row[0]
            distance = row[1]

            if distance > stop:
                break

            if distance >= start and distance <= stop:

                # Get delta values
                delta_dist = distance - last_distance
                delta_elevation = elevation - last_elevation

                # Get y angle in degrees
                y_angle = math.degrees(math.atan2(delta_elevation, delta_dist))

                # Get closest speed index
                closest_speed = min(speed_dict, key=lambda x:abs(x-speed))
                speed_index = speed_dict.get(closest_speed)

                # Get closest degrees index
                closest_degrees = min(degrees_dict, key=lambda x:abs(x-y_angle))
                deg_index = degrees_dict.get(closest_degrees)

                # Get avg power from closest values in power table
                power_avg = power_table[deg_index][speed_index]

                # Get estimated time for delta distance
                time = delta_dist/(speed*1000)

                # Get energy consumption of delta distance
                energy_sum += power_avg * time

                # Get fraction of power for delta distance
                #power_sum += (delta_dist/(speed*1000)) * power_avg
                power_sum += power_avg

                # Count number of calculations
                power_counter += 1

                # Assign last values
                last_distance = distance
                last_elevation = elevation

                # Increment line count
                line_count += 1

    # Get total distance
    total_dist = stop - start
    print("Total distance: " + str(total_dist) + " m")

    # Get estimated time
    time = total_dist/(speed*1000)
    time_h = int(time)
    time_m = int(time*60 - time_h*60)
    time_s = int(time*60*60 - time_h*60*60 - time_m*60)
    print("Estimated time: " + str(time_h) + ":" + str(time_m) + ":" + str(time_s))

    # Get average power consumption
    power_avg = power_sum/power_counter
    print("Average power consumption: " + str(power_avg) + ' W')

    # Get energy in watt hours
    energy = power_avg * time
    print("Total energy consumption: " + str(energy_sum) + ' Wh')