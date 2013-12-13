# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 11:50:44 2013

@author: nipun
"""
import numpy as np


def step_changes(series, threshold):
    diff_series = np.diff(series.values)
    return {"magnitude": diff_series, "times": series[np.abs(diff_series) > threshold].index}
    # Finding times at which these step changes take place


def assign_based_on_step_changes(df_mains, df_appliances, sorted_appliance_list, mapping, step_threshold=30):
    for load in sorted_appliance_list:
        if load not in mapping:
            print load
            step_load = set(
                step_changes(df_appliances[load], step_threshold)["times"])
            step_mains_1 = set(
                step_changes(df_mains.Mains_1_Power, step_threshold)["times"])
            step_mains_2 = set(
                step_changes(df_mains.Mains_2_Power, step_threshold)["times"])

            # Find intersection with Mains 1 and 2
            l1 = len(step_load.intersection(step_mains_1))
            l2 = len(step_load.intersection(step_mains_2))

            print l1, l2, len(step_load), load

            if 1.0 * l1 / len(step_load) > 0.9:
                # More than 90% events detected
                mapping[load] = 1
            elif 1.0 * l2 / len(step_load) > 0.9:
                # More than 90% events detected
                mapping[load] = 2
            else:
                print "Load %s could not be assigned" % load
        # print mapping
    return mapping


def thresholding_based_load_assignment(df_mains, df_appliances, mapping, sorted_appliance_list, converged=False, TOLERANCE=30):
    iteration = -1
    while converged == False:
        before_iteration_len_mapping = len(mapping.keys())
        iteration += 1
        for load in sorted_appliance_list:
            if load not in mapping:
                # Since mains 1 has less average load we check it first
                # Note we may need some tolerance as 1-2 values may be off, but more than 20 odd values satisying
                # would mean that we can safely assign the other mains

                c1 = len(
                    np.where((df_appliances[load].values - df_mains.Mains_1_Power.values) > 0)[0])
                c2 = len(
                    np.where((df_appliances[load].values - df_mains.Mains_2_Power.values) > 0)[0])
                # Using a copy of the Mains Minute DF rather than the original

                if c1 > TOLERANCE and c2 < TOLERANCE:
                    mapping[load] = 2
                elif c2 > TOLERANCE and c1 < TOLERANCE:
                    mapping[load] = 1

                # Subtracting Load from the assigned Mains and filling in zeros for
                # few spots where appliance value might be more due to error
            if load in mapping:
                # Load has been assined
                if mapping[load] == 1:
                    df_mains.Mains_1_Power = df_mains.Mains_1_Power - \
                        df_appliances[load]
                    df_mains.Mains_1_Power[df_mains.Mains_1_Power < 0] = 0
                else:
                    df_mains.Mains_2_Power = df_mains.Mains_2_Power - \
                        df_appliances[load]
                    df_mains.Mains_2_Power[df_mains.Mains_2_Power < 0] = 0

        # print "After iteration %d" %iteration
        # print mapping
        after_iteration_len_mapping = len(mapping.keys())
        if after_iteration_len_mapping == before_iteration_len_mapping:
            converged = True

    return mapping


def assign_load_to_mains(df_mains, df_appliances):
    appliance_peak_power_dict = {}
    for appliance in df_appliances:
        appliance_peak_power_dict[appliance] = df_appliances[appliance].max()
        # This variable is named 's' in the algorithm described in the paper
    sorted_appliance_list = sorted(appliance_peak_power_dict,
                                   key=appliance_peak_power_dict.get, reverse=True)
    mapping = {}
    df_mains_copy = df_mains.copy()
    mapping = thresholding_based_load_assignment(
        df_mains_copy, df_appliances, mapping, sorted_appliance_list, False, 300)
    mapping = assign_based_on_step_changes(
        df_mains, df_appliances, sorted_appliance_list, mapping)
    return mapping
