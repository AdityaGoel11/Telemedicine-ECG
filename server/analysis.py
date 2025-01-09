import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from datetime import datetime
measures = {}
column_names=['Time','ECG']

dataset = pd.read_csv('D:/ECGdata33.csv',names=column_names,sep=',',skiprows=50,skipfooter=50, engine='python')

dataset = dataset.tail(-1)

dataset.Time=dataset.Time/1000
hrw = 0.75
fs = 40
# dataset.describe()
# dataset.info()
dataset.head()
# dataset.cumsum
#plt.figure()
#plt.show()

# dataset.tail()
plt.plot(dataset.Time,dataset.ECG)
plt.show()
dataset.hist()
plt.show()
mov_avg = dataset['ECG'].rolling(int(hrw*fs)).mean()
avg_hr = (np.mean(dataset.ECG))
mov_avg = [avg_hr if math.isnan(x) else x for x in mov_avg]
# mov_avg = [x*1.2 for x in mov_avg] #For now we raise the average by 20% to prevent the secondary heart contraction from interfering, in part 2 we will do this dynamically
dataset['ECG_rollingmean'] = mov_avg #Append the moving average to the dataframe
#Mark regions of interest
window = []
peaklist = []
listpos = 1 #We use a counter to move over the different data columns
for datapoint in dataset.ECG:
    rollingmean = dataset.ECG_rollingmean[listpos] #Get local mean
    if (datapoint <= rollingmean) and (len(window) <= 1): #If no detectable R-complex activity -> do nothing
        listpos += 1
    elif (datapoint > rollingmean): #If signal comes above local mean, mark ROI
        window.append(datapoint)
        print("datapoints are :", datapoint)
        listpos += 1
    else: #If signal drops below local mean -> determine highest point
        maximum = max(window)
        beatposition = listpos - len(window) + (window.index(max(window))) #Notate the position of the point on the X-axis
        peaklist.append(beatposition)#Add detected peak to list
        print("beat position is : ", beatposition)
        window = [] #Clear marked ROI
        listpos += 1
# CALCULATE BPM: DISPLAY RR LIST, RR INTERVAL, AVG BPM
rr_list = []
cnt = 0
rr_interval = 0
while cnt < (len(peaklist) - 1):
    rr_interval = (peaklist[cnt + 1] - peaklist[cnt])  # Calculate distance between beats in number of samples
    ms_dist = ((rr_interval / fs) * 1000.0)  # Convert sample distances to ms distances
    rr_list.append(ms_dist)  # Append to list
    cnt += 1

bpm = 60000 / np.mean(rr_list)  # 60000 ms (1 minute) / average R-R interval of signal

print("RR List:", rr_list)
print("RR Intervals:", rr_interval)
print("Average Heart Beat: %.1f BPM" % bpm)
# PLOTTING :
ybeat = [dataset.ECG[x] for x in peaklist] #Get the y-value of all peaks for plotting purposes
plt.title("Detected peaks in signal")
plt.xlim(0,2500)
plt.plot(dataset.ECG, alpha=0.5, color='blue', label = "raw signal")
# PLOTTING MOVING AVERAGE:
plt.plot(mov_avg, color ='green', label = "moving average")
# PLOTTING DETECTED PEAKS:
plt.scatter(peaklist, ybeat, color='red', label = "average : %.1f BPM"%bpm)
plt.legend(loc= 4, framealpha= 0.6)
plt.show()
