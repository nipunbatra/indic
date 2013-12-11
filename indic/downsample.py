# -*- coding: utf-8 -*-



def downsample(df,window='1Min',how='mean'):
    return df.resample(window,how).dropna()
   
