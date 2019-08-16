from tkinter import *
import csv
import math
import enum 
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
mpl.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

# Create main window
root = Tk()
#root.geometry("800x400+0+0")
root.title("Energy Consumption Calculator")

# Create frame for input and calculation
inputFrame = Frame(root, width=600, height=300)
inputFrame.grid(row=0, column=0, padx=25)

# Create frame for graph
graphFrame = Frame(root)
graphFrame.grid(row=0, column=1)

# Inputs
# Start
label_start = Label(inputFrame, text="Starting point (m)")
label_start.grid(row=0, column=0, sticky=E)

entry_start = Entry(inputFrame)
entry_start.grid(row=0, column=1)

# Destination
label_dest = Label(inputFrame, text="Destination (m)")
label_dest.grid(row=1, column=0, sticky=E)

entry_dest = Entry(inputFrame)
entry_dest.grid(row=1, column=1)

# Speed
label_speed = Label(inputFrame, text="Speed (km/h)")
label_speed.grid(row=2, column=0, sticky=E)

entry_speed = Entry(inputFrame)
entry_speed.grid(row=2, column=1)

# Total distance
label_distance = Label(inputFrame, text="Total distance (m)")
label_distance.grid(row=3, column=0, sticky=E)

entry_distance = Entry(inputFrame)
entry_distance.grid(row=3, column=1)

# Estimated time
label_time = Label(inputFrame, text="Estimated time (h:m:s)")
label_time.grid(row=4, column=0, sticky=E)

entry_time = Entry(inputFrame)
entry_time.grid(row=4, column=1)

# Average power consumption
label_power = Label(inputFrame, text="Average power consumption (W)")
label_power.grid(row=5, column=0, sticky=E)

entry_power = Entry(inputFrame)
entry_power.grid(row=5, column=1)

# Average energy consumption
label_energy = Label(inputFrame, text="Total energy consumption (Wh)")
label_energy.grid(row=6, column=0, sticky=E)

entry_energy = Entry(inputFrame)
entry_energy.grid(row=6, column=1)

def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
    xvalue = int(event.xdata)
    entry_start.delete(0, END)
    entry_start.insert(0,str(xvalue))
def onrelease(event):
    print('%s release: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
    xvalue = int(event.xdata)
    entry_dest.delete(0, END)
    entry_dest.insert(0,str(xvalue))

def Calculate():
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
    start = int(entry_start.get())      #int(input("Type start in meter: "))
    stop = int(entry_dest.get())        #int(input("Type stop in meter: "))
    speed = int(entry_speed.get())      #int(input("Type in speed in kmh: "))

    # Reset variables
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
        entry_distance.delete(0, END)
        entry_distance.insert(0, str(total_dist))

        # Get estimated time
        time = total_dist/(speed*1000)
        time_h = int(time)
        time_m = int(time*60 - time_h*60)
        time_s = int(time*60*60 - time_h*60*60 - time_m*60)
        print("Estimated time: " + str(time_h) + ":" + str(time_m) + ":" + str(time_s))
        entry_time.delete(0, END)
        entry_time.insert(0, str(time_h) + ":" + str(time_m) + ":" + str(time_s))

        # Get average power consumption
        power_avg = power_sum/power_counter
        print("Average power consumption: " + str(power_avg) + ' W')
        entry_power.delete(0, END)
        entry_power.insert(0, str(power_avg))

        # Get energy in watt hours
        energy = power_avg * time
        print("Total energy consumption: " + str(energy_sum) + ' Wh')
        entry_energy.delete(0, END)
        entry_energy.insert(0, str(energy_sum))

def Reset():
    entry_start.delete(0, END)
    entry_dest.delete(0, END)
    entry_speed.delete(0, END)
    entry_distance.delete(0, END)
    entry_time.delete(0, END)
    entry_power.delete(0, END)
    entry_energy.delete(0, END)
def CreateFigure():
    fig = plt.figure()
    fig.canvas.callbacks.connect('button_press_event', onclick)
    fig.canvas.callbacks.connect('button_release_event', onrelease)
    a = fig.add_subplot(111)
    checkpoint_list = [0,322,588,633,988,1211,1496,1766,1786,2178,2432,2719,3022]
    checkpoint_list = [x * 1000 for x in checkpoint_list]
    yvalue = [50,50,50,50,50,50,50,50,50,50,50,50,50]

    for (checkpointname, checkpoint) in zip(checkpoint_name_list,checkpoint_list):
        a.annotate(str(checkpointname), xy=(checkpoint*1000, 100), xytext=(checkpoint*1000, 200),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )
    a.scatter(checkpoint_list,yvalue,c=np.random.rand(13))
    a.plot(distance_list, elevation_list)
    plt.show()
# Buttons
button_rst = Button(inputFrame, text="Open Chart", command=CreateFigure, bg="deepsky blue", fg="white")
button_rst.grid(row=7, column=0, sticky=W+E, padx=2, pady=1)

button_calc = Button(inputFrame, text="Calculate", command=Calculate, bg="deepsky blue", fg="white")
button_calc.grid(row=7, column=1, sticky=W+E, padx=2, pady=1)

button_rst = Button(inputFrame, text="Reset", command=Reset, bg="red2", fg="white")
button_rst.grid(row=7, column=2, sticky=W+E, padx=2, pady=1)



# Draw graph
# Read file
line_count = 0
elevation_list = []
distance_list = []
checkpoint_name_list = ["Darwin","Katherine","Daly Waters","Dunmarra","Dunmarra","Barrow Creek","Alice Springs","Kulgera","NT / SA Border","Coober Pedy","Glendambo","Port Augusta","Adelaide",]

with open('wsc_elevation_solbritt_2015.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    
    for row in csv_reader:
        if line_count == 0:
            line_count += 1 
        else:
            
            if row[2] == '':
                continue

            # Convert all items to floats    
            row = [x.replace(',','.') for x in row]          
            row = [float(x) for x in row]

            # Get elevation and distance
            elevation_list.append(row[0])
            distance_list.append(row[1])

            # Increment line count
            line_count += 1

root.mainloop()