# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 13:26:36 2013

@author: nipun
"""
import numpy as np
from copy import deepcopy


def calibrate_centroids(df_mains_train, df_appliances_train, labels_appliance, centroids, loads_to_mains_mapping):
    calib_centroids = deepcopy(centroids)
    for appliance in labels_appliance:
            l = labels_appliance[appliance]
            print "%s has %d states" % (appliance, max(l) + 1)

            # Finding factors for 2,..K th state
            # Note here indexing starts from 0 and not 1
            for k in range(1, max(l) + 1):
                # Finding idx of where appliance is in state k-1 and next state
                # is k
                idx = []
                for i in range(len(l) - 1):
                    if l[i] == k - 1 and l[i + 1] == k:
                        idx.append(i)
                        diff_appliance = np.diff(
                            df_appliances_train[appliance].values)
                        diff_mains_1 = np.diff(
                            df_mains_train.Mains_1_Power.values)
                        diff_mains_2 = np.diff(
                            df_mains_train.Mains_2_Power.values)

                        if loads_to_mains_mapping[appliance] == 1:
                            x = 1.0 * diff_mains_1[idx] / diff_appliance[idx]
                            x = x[x < 2]
                            x = x[x > 0]
                        else:
                            x = 1.0 * diff_mains_2[idx] / diff_appliance[idx]
                            x = x[x < 2]
                            x = x[x > 0]
                # print np.average(x),appliance
                if (np.average(x) < 0.9 or np.average(x) > 1.1) and len(x) > 10:
                    calib_centroids[appliance][k] = centroids[
                        appliance][k] * np.average(x)

            # print "Average for %s in %dth state is %f and number of
            # transitions was %d" %(appliance,k+1,np.average(x),len(idx))
    for appliance in calib_centroids:
        calib_centroids[appliance] = list(
            np.array(calib_centroids[appliance]).astype(int))
    return calib_centroids
