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
line_count = 0

# Read file
with open('log.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names')
            line_count += 1
        else:
            # Convert all items to floats   
            row[1] = row[1].replace(',','.')            
            row = [float(x) for x in row]

            # Get power
            volt = row[15]
            current = row[16]
            power = volt * current

            # Get speed
            speed = row[24]

            # Get y angle
            x_acc_val = row[30]
            y_acc_val = row[31]
            z_acc_val = row[32]

            x2 = x_acc_val * x_acc_val
            y2 = y_acc_val * y_acc_val
            z2 = z_acc_val * z_acc_val

            result = math.sqrt(x2 + z2)
            result = y_acc_val / result
            y_angle = math.atan(result)

            # Get closest speed index
            closest_speed = min(speed_dict, key=lambda x:abs(x-speed))
            speed_index = speed_dict.get(closest_speed)
            
            # Get closest degrees index
            closest_degrees = min(degrees_dict, key=lambda x:abs(x-y_angle))
            deg_index = degrees_dict.get(closest_degrees)
            
            # Insert and sum to power table
            power_table[deg_index][speed_index] += power

            # Increment line count
            line_count += 1

    # All rows done
    # Calculate average of all values
    for i in range(rows):
        for j in range(columns):
            power_table[i][j] /= line_count

    print(f'Completed - Processed {line_count} lines')

    # Create dataframe from 2d array
    df = pd.DataFrame(power_table)
    df.columns = speed_dict
    df.index = degrees_dict

    # Plot on graph
    y = range(df.shape[0])
    x = range(df.shape[1])
    x, y = np.meshgrid(x, y)

    graph = plt.figure().gca(projection='3d')
    graph.plot_wireframe(y, x, df)

    plt.show()
    
    # Write to new file
    with open("power_table.csv", "w+", newline='') as my_csv:
        df.to_csv(my_csv, sep=';')

    print(df)