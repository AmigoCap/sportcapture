# -*- coding: utf-8 -*-
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
import pandas as pd
import math
import os.path
from utils import read_from_mkr

def read_from_csv(filename, patientname, markers) : 
    """
    Read marker datas from csv file exported by Nexus
    return a dict with keys - marker names, values - coord data
    """
    datas = dict()
    frames = 0
    result = pd.read_csv(filename,sep=',',encoding='utf-8',skiprows=2,low_memory=False)

    for marker in markers :
        try:
            col = result.columns.get_loc(patientname+':'+marker)
        except Exception as e:
            print('read error : ' + marker)
            continue
        data_one_marker = result.ix[:, col : col + 3]
        marker_data = dict()
        marker_data['x'] = [float(x) for x in data_one_marker.ix[2:,0].tolist()]
        marker_data['y'] = [float(x) for x in data_one_marker.ix[2:,1].tolist()]
        marker_data['z'] = [float(x) for x in data_one_marker.ix[2:,2].tolist()]
        if len(marker_data['x']) > frames :
            frames = len(marker_data['x'])
        datas[marker] = marker_data
    return datas, frames

datafolder = '../data/'
filename = 'Arnaud Cal 02'
fullpath = datafolder + filename
patientname = 'Arnaud'
mkrpath = datafolder + patientname + '.mkr'

if os.path.isfile(mkrpath) :
    markers, lines = read_from_mkr(mkrpath)
else :
    # all marker names
    markers = ['RFHD','RBHD','LBHD','LFHD','C7','RBAK','RSHO','RUPA','RELB','RFRA','RFRM','RWRA','LFRM','RWRB','RFIN','CLAV','LSHO','LUPA','LELB',
                'LFRA','LWRB','LWRA','LFIN','STRN','T10','RPSI','LPSI','RASI','LASI','RTHI','RKNE','RTIB','RANK','RHEE','RTOE','LTHI','LKNE',
                'LTIB','LHEE','LANK','LTOE']

    # connectivity between markers, each one represents a line in animation
    lines = [['RFHD','LFHD'],['RFHD','RBHD'],['LFHD','LBHD'],['RBHD','LBHD'],
    ['RFHD','C7'],['LFHD','C7'],['RBHD','C7'],['LBHD','C7'],['C7','RSHO'],['C7','LSHO'],
    ['RSHO','RUPA'],['RUPA','RELB'],['RELB','RFRM'],['RFRM','RWRA'],['RFRM','RWRB'],['RFIN','RWRA'],['RFIN','RWRB'],['RSHO','T10'],['RSHO','CLAV'],
    ['LSHO','LUPA'],['LUPA','LELB'],['LELB','LFRM'],['LFRM','LWRA'],['LFRM','LWRB'],['LFIN','LWRA'],['LFIN','LWRB'],['LSHO','T10'],['LSHO','CLAV'],
    ['CLAV','STRN'],['C7','RBAK'],['T10','RBAK'],
    ['STRN','RASI'],['STRN','LASI'],['T10','RPSI'],['T10','LPSI'],
    ['RPSI','RASI'],['LPSI','LASI'],['LPSI','RPSI'],
    ['RASI','RTHI'],['RPSI','RTHI'],['LASI','LTHI'],['LPSI','LTHI'],
    ['RTHI','RKNE'],['RKNE','RTIB'],['RTIB','RANK'],['RTIB','RHEE'],['RANK','RHEE'],['RTOE','RANK'],['RTOE','RHEE'],
    ['LTHI','LKNE'],['LKNE','LTIB'],['LTIB','LANK'],['LTIB','LHEE'],['LANK','LHEE'],['LTOE','LANK'],['LTOE','LHEE'],
    ['RELB','RFRA'],['RFRA','RWRA'],['RFRA','RWRB'],
    ['LELB','LFRA'],['LFRA','LWRA'],['LFRA','LWRB']]

datas, frames = read_from_csv(fullpath+'.csv', patientname, markers)
## GL View widget to display data
app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('Amigo : Skeleton Animation')

ax = gl.GLAxisItem()
ax.setSize(3000,3000,3000)
w.addItem(ax)
w.setCameraPosition(distance=4000)

# store lines
plot_obj = []
for line in lines :
    obj = gl.GLLinePlotItem()
    w.addItem(obj)
    plot_obj.append(obj)

index = 0
def update():
    global lines, plot_obj, index, frames, w

    print(str(index)+'/'+str(frames), end="\r")
    for line,obj in zip(lines,plot_obj) :
        #print(line)
        try:
            # line[0] marker name of one end of the line
             x1 = datas[line[0]]['x'][index] 
             y1 = datas[line[0]]['y'][index]
             z1 = datas[line[0]]['z'][index]
        except Exception as e:
            print('0get error : '+line[0], end="\r")
            obj.setData(pos=np.array([[0,0,0],[0,0,0]]))
            continue
        try:
            # line[1] marker name of the other end of the line
            x2 = datas[line[1]]['x'][index]
            y2 = datas[line[1]]['y'][index]
            z2 = datas[line[1]]['z'][index]
        except Exception as e:
            print('1get error : '+line[1], end="\r")
            obj.setData(pos=np.array([[0,0,0],[0,0,0]]))
            continue

        if (math.isnan(x1) or math.isnan(y1) or math.isnan(z1) or math.isnan(x2) or math.isnan(y2) or math.isnan(z2)) : 
            #print('nan error ' + str(num),end="\r")
            obj.setData(pos=np.array([[0,0,0],[0,0,0]]))
            continue
        points = np.array([[x1,y1,z1],[x2,y2,z2]])
        obj.setData(pos=points, mode='lines')
    index = (index+1) % frames
    return
    
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(15)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
