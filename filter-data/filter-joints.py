#!/usr/bin/python

from math import sqrt

#change here the file from which to read the data
filename = "../data/rugby+angle.csv"

def smoothSeries (series) :
    "This function smooths the given time series"
    smoothedSeries = []
    for i,serie in enumerate(series) :
        for j,value in enumerate(serie) :
            if j == 0 :
                smoothedSeries.append([])
                smoothedSeries[i].append(value)
            elif j < len(serie) - 1 :
                smoothedSeries[i].append(0.21 * serie[j-1] + 0.58 * serie[j] + 0.21 * serie[j+1])
            else :
                smoothedSeries[i].append(value)
    return smoothedSeries;


def differentiateSeries (series, frameRate) :
    "This function differentiates the given time series"
    diff = []
    for i,serie in enumerate(series) :
        for j,value in enumerate(serie) :
            if j == 0 :
                diff.append([])

            if j > 1 and j < len(serie) - 2 :
                diff[i].append(frameRate*(-serie[j-2]+8*serie[j-1]-8*serie[j+1]+serie[j+2])/12);
            elif j>1 :
                diff[i].append(frameRate*(serie[j]-serie[j-1]))
            else :
                diff[i].append(frameRate*(serie[j+1]-serie[j]))
    return diff;

def norm2OfSeries (series, firstIndex, numberOfSeries) :
    "This function computes the norm 2 of the series between firstIndex and firstIndex+numberOfseries in series"
    norm = []
    for j, value in enumerate(series[firstIndex]) :
        sum = 0
        for i in range(firstIndex, firstIndex+numberOfSeries) :
            sum += series[i][j]*series[i][j]
        norm.append(sqrt(sum))
    return norm;





# read the whole files
fileObject = open(filename, 'r')
fileLines = fileObject.readlines()

started = False
content = []



for line in fileLines :
    if 'Joints' in line :
        # look for the line starting the data
        started = True
    elif started and  line.strip() == "" :
        # we reached the end of the data
        started = False
    elif started :
        # append the line to the data array
        content.append(line.strip())

# extract the first few lines which are metadata
frameRate = int(content.pop(0))
names = content.pop(0).split(',')
headers = content.pop(0).split(',')
units = content.pop(0).split(',')
# at this point, the rest of the file is pure data

# we now need data as time series for each measure.
timeSeries = []
namesToDrop = []
for i,line in enumerate(content) :
    a = line.split(',')
    for j,mesure in enumerate(a) :
        if i == 0 :
            timeSeries.append([])
            if mesure == '' :
                namesToDrop.append(j)
        if mesure == '' :
            timeSeries[j].append(0)
        else :
            timeSeries[j].append(float(mesure))

# we now need to smooth each time serie using gaussian blur
timeSeriesSmoothed = smoothSeries(timeSeries)

# we now need to differiate the series to create speed and then acceleration
speedSeries = differentiateSeries(timeSeriesSmoothed, frameRate)
accelerationSeries =  differentiateSeries(speedSeries, frameRate)

# for each joint, compute the norm of vitesse and acceleration
result = {}
for i,name in enumerate(names) :
    if name != '' and i not in namesToDrop :
        startOfName = 0
        if ':' in name :
            startOfName = name.index(':')+1
        #name without prefix
        goodName = name[startOfName:];
        result[goodName] = {}
        # look if the data is 1D, 2D or 3D
        number = 1
        if names[i+1] == '' :
            number = 2
        if names[i+2] == '' :
            number = 3
        # apply the norm to reduce the nD values to a single dimension value
        result[goodName]['angle'] = norm2OfSeries(timeSeriesSmoothed, i, number)
        result[goodName]['angular_speed'] = norm2OfSeries(speedSeries, i, number)
        result[goodName]['angular_acceleration'] = norm2OfSeries(accelerationSeries, i, number)

# now we need to save the result in a json file
# a little tweek is necessary to export only 2 digits after the point, we don't need more precision and it saves a lot of size
import json
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.2f')

# the output file is simply the file name with the '_filtered' suffix
with open(filename[:-4]+'_filtered.json', 'w') as outfile:
    json.dump(result, outfile)

print('done !')
