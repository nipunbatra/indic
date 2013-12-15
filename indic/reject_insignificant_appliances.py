# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 11:34:33 2013

@author: nipun
"""


def reject_insignificant_appliance(df_appliances, min_power_threshold=25, min_contribution_threshold=1):
    reject_list = []
    contribution_df = df_appliances.sum() * 100.0 / df_appliances.sum().sum()
    for appliance in df_appliances:
        if df_appliances[appliance].max() < min_power_threshold:
            print "%s will be deleted since it's max power=%f is less than threshold" % (appliance, df_appliances[appliance].max())
            reject_list.append(appliance)
    for appliance in df_appliances:
        if appliance not in reject_list:
            if contribution_df[appliance] < min_contribution_threshold:
                print "%s will be deleted since it's contribution=%f is less than threshold" % (appliance, contribution_df[appliance])
                reject_list.append(appliance)

    for appliance in reject_list:
        del df_appliances[appliance]
    return df_appliances
