import pandas as pd
import numpy as np

def read_from_csv(filename, patientname, markers) : 
    """
    Read marker datas from csv file exported by Nexus
    return a pandas Dataframe with marker name and x,y,z as row, frame as column
    """
    result = pd.read_csv(filename,sep=',',encoding='utf-8',skiprows=2,low_memory=False).convert_objects(convert_numeric=True)
    frames = result.shape[0]-2
    datas = pd.DataFrame(columns=range(frames), index=pd.MultiIndex.from_product([markers,['x','y','z']]))

    for marker in markers :
        try:
            col = result.columns.get_loc(patientname+':'+marker)
        except Exception as e:
            print('read error : ' + marker)
            continue
        data_one_marker = result.ix[:, col : col + 3]
        datas.loc[marker,'x'][0:data_one_marker.T.shape[1]] = data_one_marker.T.ix[0,2:]
        datas.loc[marker,'y'][0:data_one_marker.T.shape[1]] = data_one_marker.T.ix[1,2:]
        datas.loc[marker,'z'][0:data_one_marker.T.shape[1]] = data_one_marker.T.ix[2,2:]
    return datas.convert_objects(convert_numeric=True), frames

def read_from_mkr(filename) :
    """
    Read marker list and segment information from .mkr file
    return markers - list of marker names, segments - list of segment in form of [start marker name, end marker name]
    """
    reading_segment = False
    markers = []
    segments = []

    with open(filename, 'r') as f :
        for line in f :
            if line == '!MKR#2\n' or line == '[Display]\n' :
                continue
            if line == '\n' :
                reading_segment = True
                continue
            if reading_segment :
                line = line[0:-1]
                segments.append(line.split(','))
            else :
                markers.append(line[0:-1])

    return markers, segments

def read_from_json(filename) :
    """
    Read joint angular information from .json file

    """
    correspondance = {
                      'L_Collar_L_Humerus' : ['LSHO'],
                      'L_Elbow_L_Wrist' : ['LWRA','LWRB'],
                      'L_Femur_L_Tibia' : ['LKNE'],
                      'L_Humerus_L_Elbow' : ['LELB'],
                      'L_Tibia_L_Foot' : ['LANK'],
                      'LowerBack_Head' : ['C7'],
                      'LowerBack_L_Collar' : ['CLAV'],
                      'LowerBack_R_Collar' : ['CLAV'],
                      'R_Collar_R_Humerus' : ['RSHO'],
                      'R_Elbow_R_Wrist' : ['RWRA','RWRB'],
                      'R_Femur_R_Tibia' : ['RKNE'],
                      'R_Humerus_R_Elbow' : ['RELB'],
                      'R_Tibia_R_Foot' : ['RANK'],
                      'Root_L_Femur' : ['LASI','LPSI'],
                      'Root_R_Femur' : ['RASI','RPSI']
                      }
    useful_joint_names = list(correspondance.keys())

    table = pd.read_json(filename)
    joints = table[useful_joint_names]

    return joints, correspondance
