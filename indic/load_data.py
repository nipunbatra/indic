# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 20:46:26 2013

@author: nipun
"""

import numpy as np
import pandas as pd
from collections import OrderedDict

def load_labels(path):
    labels=OrderedDict()
    labels_file_rec=np.loadtxt("%s/labels.dat" %path,
                               dtype={'names':['id','appliance'],
                                      'formats':['i2','S20']})
    for i in range(2,len(labels_file_rec)):
        labels[i]=labels_file_rec[i][1]
    return labels                                      


def load_mains_data(path):
    mains_1_data=np.loadtxt('%s/channel_1.dat' %path)
    mains_2_data=np.loadtxt('%s/channel_2.dat' %path)
    mains_1_power=mains_1_data[:,1]
    mains_2_power=mains_2_data[:,1]
    timestamp=mains_1_data[:,0]
    timestamp_mains_date=timestamp.astype('datetime64[s]')
    df_mains=pd.DataFrame({'Mains_1_Power':mains_1_power,
                           'Mains_2_Power': mains_2_power},
                           index=timestamp_mains_date)
    return df_mains

def load_appliances_data(path,labels_dict):
    appliance_power_dict=OrderedDict()
    timestamp=np.loadtxt('%s/channel_3.dat' %path)[:,0]
    timestamp_appliance_date=timestamp.astype('datetime64[s]')
    for i in labels_dict:
        appliance_power_dict[labels_dict[i]]=np.loadtxt('%s/channel_%d.dat' %(path,i+1))[:,1]
    df_appliances=pd.DataFrame(appliance_power_dict,index=timestamp_appliance_date)
    return df_appliances
    
    
    
                               
