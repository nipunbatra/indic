# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 20:45:22 2013

@author: nipun
"""
import numpy as np
import pandas as pd


def find_intersection(df_mains, df_appliances):
    """Returns the DatetimeIndex of intersection of mains and appliances

    Parameters
    ----------
    df_mains : pandas.DataFrame
    df_appliances : pandas.DataFrame

    Returns
    -------
    DatetimeIndex
    """
    return pd.Index(np.sort(list(set(df_mains.index).intersection(set(df_appliances.index)))))


def find_contigous_times(df, difference=1000):
    """
    Creates a list of type [(start_time, end_time)]
    where each tuple has contiguous data separated.
    Two consecutive tuples are separated by `difference`
    seconds

    Parameters
    ----------
    df : pandas.DataFrame
    difference : int, default=1000
        Maximum gap (in seconds) between readings to chop of a 
        contiguous time slot
    """
    idx = np.where(np.diff(df.index.values) / 1e9 > difference)[0]
    if idx.size == 0:
        # Whole data is contiguous
        return [(df.index.values[0], df.index.values[-1])]
    else:
        contiguous_time_tuples = []
        start = 0
        for end in idx:
            contiguous_time_tuples.append(
                (df.index.values[start], df.index.values[end]))
            start = end + 1
        return contiguous_time_tuples
