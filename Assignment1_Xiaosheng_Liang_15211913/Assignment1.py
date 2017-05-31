import os
import urllib.request
import pandas as pd
import requests
import matplotlib
import matplotlib.pyplot as plt 
import json
from pandas.tools.plotting import scatter_matrix

api_key = "494cf3bcc5870fa4"

def get_raw_data(file_loc, api_key, location, year, month, day):
    if month <10: 
        month = "0" + str(month)
    else:
        month = str(month)
    if day <10: 
        day = "0" + str(day)
    else:
        day = str(day)
    link = "http://api.wunderground.com/api/"+api_key + "/history_"+ str(year)+ month + day + "/q/"+ location + ".json"
    # http://api.wunderground.com/api/494cf3bcc5870fa4/history_20161010/q/CA/San_Francisco.json
    get_and_write_data(link, file_loc)  

def get_and_write_data(link, file_loc): 
    response = urllib.request.urlopen(link)
    html = response.read().decode()
    data_dic = json.loads(html)
    with open(file_loc,"w") as json_file:
    	json_file.write(json.dumps(data_dic))

def read_file(file_loc):
    with open(file_loc,"r") as json_file:
	    data = pd.read_json(json_file)
    return data

        
# collect the data
location = "CA/San_Francisco"
raw_file_loc = "weather-data-raw.txt"
year = 2016
month = 10
day = 10
get_raw_data(raw_file_loc, api_key, location, year, month, day)
data = read_file(raw_file_loc)
data = data["history"][3]
print ("collection finished!")


# parse the collected data and store in dataframes
time = []
tempm = []
tempi = []
dewpti = []
wspdm = []
pressurei = []
for i in range(0,24):
    time.append(pd.to_datetime(data[i]["date"]["pretty"]))
    tempm.append(float(data[i]["tempm"]))
    tempi.append(float(data[i]["tempi"]))
    dewpti.append(float(data[i]["dewpti"]))
    wspdm.append(float(data[i]["wspdm"]))
    pressurei.append(float(data[i]["pressurei"]))


# store data in dataframes
frame0 = pd.DataFrame({"tempm":tempm, "tempi":tempi},index = time)
frame0 = frame0.sort_index(axis=1,ascending=True) # sort the data based on time
frame1 = pd.DataFrame({"dewpti":dewpti, "tempi":tempi},index = time) 
frame2 = pd.DataFrame({"wspdm":wspdm, "tempi":tempi},index = time) 
frame3 = pd.DataFrame({"tempm":tempm, "tempi":tempi, "wspdm":wspdm, "dewpti":dewpti},index = time) 
frame4 = pd.DataFrame({"tempm":tempm, "pressurei":pressurei},index = time)


# Line Graph
frame0.plot()
plt.title("Hourly Tempm and Tempi in San_Francisco on October 10, 2016\n")
plt.ylabel("Tempm | Tempi")
plt.xlabel("Time")
print ("line graph is finished.")

# Area Graph
frame0.plot.area(stacked = False)
plt.title("Hourly Tempm and Tempi in San_Francisco on October 10, 2016\n")
plt.ylabel("Tempm | Tempi")
plt.xlabel("Time")
print ("Area graph is finished.")

# Stacked Histogram
frame1.plot.hist(stacked=True)
plt.title("Hourly Tempm and Dewpti in San_Francisco on October 10, 2016")
plt.ylabel("Dewpti | Tempi")
plt.xlabel("Time")
print ("Histogram is finished.")

# ScatterPlots
frame0.plot.scatter(x="tempm", y="tempi", s=50 )
plt.title("Hourly Tempi and Tempi in San_Francisco on October 10, 2016\n")
plt.ylabel("Tempm")
plt.xlabel("Tempi")
plt.show()

plt.scatter(frame2['wspdm'], frame0['tempm'])
plt.title("Hourly Wspdm and Tempi in San_Francisco on October 10, 2016\n")
plt.ylabel("Tempm")
plt.xlabel("Wspdm")
print ("ScatterPlots are finished.")

# Matrix Graph
scatter_matrix(frame2, alpha=0.2, figsize=(6, 6), diagonal='kde')

scatter_matrix(frame3, alpha=0.2, figsize=(6, 6), diagonal='kde')
print ("Matrix Graphs are finished")

# Dual Axis Line Graphs
ax = frame2.plot(secondary_y=['tempi'])
ax.set_ylabel("Wspdm")
ax.right_ax.set_ylabel("Tempi")
plt.title("Hourly Tempi and Wspdm in San_Francisco on October 10, 2016\n")
plt.xlabel("Time")

frame2.plot(subplots=True, figsize=(6, 6));
print ("Dual Axis Line Graphs are finiished!")

# Explore the data further
avg_hourly_tempm = frame4.groupby("tempm") 
temp_data = avg_hourly_tempm.mean()
print ("Data for Average of Pressure as Temperature increases:")
print(temp_data)
temp_data.plot()
plt.title("Average of Pressure as Temperature increases\n")
plt.xlabel("Temperature")
plt.ylabel("Pressure")
plt.show()

