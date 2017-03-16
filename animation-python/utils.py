import pandas as pd
import numpy as np

def read_from_csv(filename, patientname, markers) : 
    """
    Read marker datas from csv file exported by Nexus
    return a dict with keys - marker names, values - coord data
    """
    result = pd.read_csv(filename,sep=',',encoding='utf-8',skiprows=2,low_memory=False).convert_objects(convert_numeric=True)
    frames = result.shape[0]-2
    datas = pd.DataFrame(columns=range(frames), index=pd.MultiIndex.from_product([markers,['x','y','z']]))

    for marker in markers :
        try:
            col = result.columns.get_loc(patientname+':'+marker+'1')
        except Exception as e:
            print('read error : ' + marker)
            continue
        data_one_marker = result.ix[:, col : col + 3]
        datas.loc[marker,'x'][0:data_one_marker.T.shape[1]] = data_one_marker.T.ix[0,2:]
        datas.loc[marker,'y'][0:data_one_marker.T.shape[1]] = data_one_marker.T.ix[1,2:]
        datas.loc[marker,'z'][0:data_one_marker.T.shape[1]] = data_one_marker.T.ix[2,2:]
    return datas.convert_objects(convert_numeric=True), frames