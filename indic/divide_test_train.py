# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 11:08:40 2013

@author: nipun
"""
from math import floor


def partition_train_test(df_mains, df_appliances, train_percentage=50):
    assert(df_mains.index.size == df_appliances.index.size)
    train_index_max = floor(df_mains.index.size * train_percentage / 100.0)
    df_train_mains = df_mains[:train_index_max]
    df_train_appliances = df_appliances[:train_index_max]
    df_test_mains = df_mains[train_index_max + 1:]
    df_test_appliances = df_appliances[train_index_max + 1:]
    return [df_train_mains, df_train_appliances, df_test_mains, df_test_appliances]
