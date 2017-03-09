import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import math


def read_from_csv(filename, markers) : 
    """
    Read marker datas from csv file exported by Nexus
    return a dict with keys - marker names, values - coord data
    """
    result = pd.read_csv(filename,sep=',',encoding='utf-8',skiprows=2,low_memory=False).convert_objects(convert_numeric=True)
    frames = result.shape[0]-2
    datas = pd.DataFrame(columns=range(frames), index=pd.MultiIndex.from_product([markers,['x','y','z']]))

    for marker in markers :
        try:
            col = result.columns.get_loc('film:'+marker)
        except Exception as e:
            print('read error : ' + marker)
            continue
        data_one_marker = result.ix[:, col : col + 3]
        datas.loc[marker,'x'][0:data_one_marker.T.shape[1]] = data_one_marker.T.ix[0,2:]
        datas.loc[marker,'y'][0:data_one_marker.T.shape[1]] = data_one_marker.T.ix[1,2:]
        datas.loc[marker,'z'][0:data_one_marker.T.shape[1]] = data_one_marker.T.ix[2,2:]
    return datas, frames

def get_speed(datas) :
    """
    Calculate the speed (per frame) of a point between the positions p0 and p1.
    Assuming v = (p(f0) - p(f1)) / (f1 - f0)
    p - tuple (x,y,z)
    f - int
    """
    v = list(map(lambda x: x / (f1-f0), [p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]]))
    return v

def get_color(v) :
    """
    Calculate rgb color according to speed value
    v - tuple (x,y,z)
    """
    speed = math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
    return (speed/10,0,0)



if __name__ == '__main__':

    filename = 'film Cal 01'

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
    ['LTHI','LKNE'],['LKNE','LTIB'],['LTIB','LANK'],['LTIB','LHEE'],['LANK','LHEE'],['LTOE','LANK'],['LTOE','LHEE']]

    datas, frames = read_from_csv(filename+'.csv', markers)

    fig = plt.figure()
    ax = p3.Axes3D(fig)

    # store lines
    plot_obj = []

    for line in lines :
        obj = ax.plot([],[],[])[0]
        plot_obj.append(obj)

    ax.set_xlim3d([-2000, 2000])
    ax.set_xlabel('X')

    ax.set_ylim3d([-1000, 2000])
    ax.set_ylabel('Y')

    ax.set_zlim3d([0, 1800])
    ax.set_zlabel('Z')

    ax.set_title('Animation')

    def update_lines(num) :
        """
        update lines on figure by reading position of markers at frame num for each line
        """
        print(str(num)+'/'+str(frames), end="\r")
        for line,obj in zip(lines,plot_obj) :
            try:
                # line[0] marker name of one end of the line
                 x1 = datas.loc[line[0],'x'][num]
                 y1 = datas.loc[line[0],'y'][num]
                 z1 = datas.loc[line[0],'z'][num]
            except Exception as e:
                print('0get error : '+line[0])
                obj.set_data([],[])
                obj.set_3d_properties([])
            try:
                # line[1] marker name of the other end of the line
                x2 = datas.loc[line[1],'x'][num]
                y2 = datas.loc[line[1],'y'][num]
                z2 = datas.loc[line[1],'z'][num]
            except Exception as e:
                print('1get error : '+line[1])
                obj.set_data([],[])
                obj.set_3d_properties([])
                continue
            if (math.isnan(x1) or math.isnan(y1) or math.isnan(z1) or math.isnan(x2) or math.isnan(y2) or math.isnan(z2)) : 
                #print('nan error ' + str(num),end="\r")
                obj.set_data([],[])
                obj.set_3d_properties([])
                continue

            obj.set_data([x1,x2],[y1,y2])
            obj.set_3d_properties([z1,z2])
            if num < datas.loc[line[0]].shape[1] :
                speed1 = get_speed((x1,y1,z1),(datas.loc[line[0],'x'][num+1],datas.loc[line[0],'y'][num+1],datas.loc[line[0],'z'][num+1]),num,num+1)
            else :
                speed1 = [0,0,0]
            obj.set_color(get_color(speed1))
            
        return plot_obj,

    line_ani = animation.FuncAnimation(fig, update_lines, frames, interval=10, blit=False)

    ax.view_init(elev=20., azim=-7)
    #line_ani.save(filename+'.mp4')
    
    plt.show()


