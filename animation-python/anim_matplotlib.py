# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import mpl_toolkits.mplot3d.axes3d as p3
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import matplotlib.animation as animation
import math
import os.path

from utils import *

if __name__ == '__main__':

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
    speed_vec = datas.ix[:,:].subtract(datas.ix[:,1:].rename(columns=lambda x: x-1))
    speed_scal = np.sqrt(np.square(speed_vec.ix[0::3].reset_index(level=1).drop('level_1',1)).add(
                         np.square(speed_vec.ix[1::3].reset_index(level=1).drop('level_1',1))).add(
                         np.square(speed_vec.ix[2::3].reset_index(level=1).drop('level_1',1)))).fillna(value=0.1).add(0.00000001)

    jet = plt.get_cmap('gist_heat') 
    norm = colors.Normalize(vmin=speed_scal.min().min(),vmax=speed_scal.max().max())
    scalarMap = cmx.ScalarMappable(norm=norm, cmap=jet)

    fig = plt.figure()
    ax = p3.Axes3D(fig)

    # store lines
    segments = []
    for line in lines :
        segments.append([(0,0,0),(0,0,0)])
    plot_obj = Line3DCollection(segments)
    ax.add_collection(plot_obj)

    #ax.set_xlim3d([-2000, 2000])
    ax.set_xlim3d([datas.ix[::3].min().min()-500, datas.ix[::3].max().max()+500])
    ax.set_xlabel('X')

    #ax.set_ylim3d([-1000, 2000])
    ax.set_ylim3d([datas.ix[1::3].min().min()-500, datas.ix[1::3].max().max()+500])
    ax.set_ylabel('Y')

    #ax.set_zlim3d([0, 1800])
    ax.set_zlim3d([datas.ix[2::3].min().min(), datas.ix[2::3].max().max()])
    ax.set_zlabel('Z')

    ax.set_title('Animation')

    def update_lines(num) :
        """
        update lines on figure by reading position of markers at frame num for each line
        """
        segments = []
        colors = []
        print(str(num)+'/'+str(frames), end="\r")
        for line in lines :
            try:
                # line[0] marker name of one end of the line
                 x1 = datas.loc[line[0],'x'][num]
                 y1 = datas.loc[line[0],'y'][num]
                 z1 = datas.loc[line[0],'z'][num]
            except Exception as e:
                print('0get error : '+line[0])

            try:
                # line[1] marker name of the other end of the line
                x2 = datas.loc[line[1],'x'][num]
                y2 = datas.loc[line[1],'y'][num]
                z2 = datas.loc[line[1],'z'][num]
            except Exception as e:
                print('1get error : '+line[1])
                
                continue

            if (math.isnan(x1) or math.isnan(y1) or math.isnan(z1) or math.isnan(x2) or math.isnan(y2) or math.isnan(z2)) : 
                #print('nan error ' + str(num),end="\r")

                continue

            segments.append(((x1,y1,z1),(x2,y2,z2)))
            colors.append(scalarMap.to_rgba(speed_scal.loc[line[0]][num]))

            plot_obj.set_segments(segments)
            plot_obj.set_color(colors)
            
        return plot_obj,

    line_ani = animation.FuncAnimation(fig, update_lines, frames, interval=10, blit=False)

    ax.view_init(elev=20., azim=-45)
    line_ani.save(filename+'.mp4')
    
    #plt.show()


