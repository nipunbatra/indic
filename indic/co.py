# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 13:43:37 2013

@author: nipun
"""
import numpy as np

import itertools


def find_nearest_index(array, value):
    idx = (np.abs(array - value)).argmin()
    return idx


def find_nearest(array, value):
    idx = (np.abs(array - value)).argmin()
    diff = array[idx] - value
    return [idx, -diff]


def find_labels(appliance_power_consumption_list, observed_power):
    labels = np.zeros(len(observed_power))
    appliance_power_consumption_array = np.array(
        appliance_power_consumption_list)
    for i in range(len(observed_power)):
        labels[i] = find_nearest_index(
            appliance_power_consumption_array, observed_power[i])
    return labels


def decode_co(length_sequence, centroids, appliance_list, states, residual_power):

    power_states_dict = {}

    co_states = {}
    co_power = {}
    total_num_combinations = 1
    for appliance in appliance_list:
        total_num_combinations *= len(centroids[appliance])

    for appliance in appliance_list:
        co_states[appliance] = np.zeros(length_sequence, dtype=np.int)
        co_power[appliance] = np.zeros(length_sequence)

    for i in range(length_sequence):
        factor = total_num_combinations
        for appliance in appliance_list:
            # assuming integer division (will cause errors in Python 3x)
            factor = factor // len(centroids[appliance])

            temp = int(states[i]) / factor
            co_states[appliance][i] = temp % len(centroids[appliance])
            co_power[appliance][i] = centroids[
                appliance][co_states[appliance][i]]

    return [co_states, co_power]


def apply_co(centroids, calib_centroids, loads_to_mains_mapping, df_mains_test):

    overall_appliance_list = [appliance for appliance in centroids]
    mains_1_appliance_list = [
        appliance for appliance in centroids if loads_to_mains_mapping[appliance] == 1]
    mains_2_appliance_list = [
        appliance for appliance in centroids if loads_to_mains_mapping[appliance] == 2]

    overall_appliance_centroids = [centroids[appliance]
                                   for appliance in overall_appliance_list]

    mains_1_appliance_centroids = [centroids[appliance]
                                   for appliance in mains_1_appliance_list]
    mains_2_appliance_centroids = [centroids[appliance]
                                   for appliance in mains_2_appliance_list]

    '''
    Case 0
    No load division
    No calibration
    '''
    appliance_list = [appliance for appliance in centroids]
    list_of_appliances_centroids = [centroids[appliance]
                                    for appliance in appliance_list]
    states_combination = list(itertools.product(*list_of_appliances_centroids))
    sum_combination = np.array(np.zeros(len(states_combination)))
    for i in range(0, len(states_combination)):
        sum_combination[i] = sum(states_combination[i])
    length_sequence = len(df_mains_test.Mains_1_Power.values)
    states = np.zeros(length_sequence)
    residual_power = np.zeros(length_sequence)
    for i in range(length_sequence):
        [states[i], residual_power[i]] = find_nearest(
            sum_combination, df_mains_test.Mains_2_Power.values[i] + df_mains_test.Mains_1_Power.values[i])
    [case_0_states, case_0_power] = decode_co(
        length_sequence, centroids, appliance_list, states, residual_power)

    '''
    Case 1
    Load division
    No calibration
    '''

    # First doing disagg. for Mains 1

    appliance_list = [
        appliance for appliance in centroids if loads_to_mains_mapping[appliance] == 1]
    list_of_appliances_centroids = [centroids[appliance]
                                    for appliance in appliance_list]
    states_combination = list(itertools.product(*list_of_appliances_centroids))
    sum_combination = np.array(np.zeros(len(states_combination)))
    for i in range(0, len(states_combination)):
        sum_combination[i] = sum(states_combination[i])
    length_sequence = len(df_mains_test.Mains_1_Power.values)
    states = np.zeros(length_sequence)
    residual_power = np.zeros(length_sequence)
    for i in range(length_sequence):

        [states[i], residual_power[i]] = find_nearest(
            sum_combination, df_mains_test.Mains_1_Power.values[i])
    [case_1_mains_1_states, case_1_mains_1_power] = decode_co(
        length_sequence, centroids, appliance_list, states, residual_power)

    appliance_list = [
        appliance for appliance in centroids if loads_to_mains_mapping[appliance] == 2]
    list_of_appliances_centroids = [centroids[appliance]
                                    for appliance in appliance_list]
    states_combination = list(itertools.product(*list_of_appliances_centroids))
    sum_combination = np.array(np.zeros(len(states_combination)))
    for i in range(0, len(states_combination)):
        sum_combination[i] = sum(states_combination[i])
    length_sequence = len(df_mains_test.Mains_1_Power.values)
    states = np.zeros(length_sequence)
    residual_power = np.zeros(length_sequence)
    for i in range(length_sequence):
        [states[i], residual_power[i]] = find_nearest(
            sum_combination, df_mains_test.Mains_2_Power.values[i])
    [case_1_mains_2_states, case_1_mains_2_power] = decode_co(
        length_sequence, centroids, appliance_list, states, residual_power)

    case_1_states = dict(case_1_mains_1_states.items()
                         + case_1_mains_2_states.items())
    case_1_power = dict(case_1_mains_1_power.items()
                        + case_1_mains_2_power.items())

    '''
    Case 2
    No Load Division
    Calibration
    '''
    appliance_list = [appliance for appliance in centroids]
    list_of_appliances_centroids = [calib_centroids[appliance]
                                    for appliance in appliance_list]
    states_combination = list(itertools.product(*list_of_appliances_centroids))
    sum_combination = np.array(np.zeros(len(states_combination)))
    for i in range(0, len(states_combination)):
        sum_combination[i] = sum(states_combination[i])
    length_sequence = len(df_mains_test.Mains_1_Power.values)
    states = np.zeros(length_sequence)
    residual_power = np.zeros(length_sequence)
    for i in range(length_sequence):
        [states[i], residual_power[i]] = find_nearest(
            sum_combination, df_mains_test.Mains_2_Power.values[i] + df_mains_test.Mains_1_Power.values[i])
    [case_2_states, case_2_power] = decode_co(
        length_sequence, centroids, appliance_list, states, residual_power)

    '''
    Case 3
    Load division
    Calibration
    '''

    # First doing disagg. for Mains 1

    appliance_list = [
        appliance for appliance in centroids if loads_to_mains_mapping[appliance] == 1]
    list_of_appliances_centroids = [calib_centroids[appliance]
                                    for appliance in appliance_list]
    states_combination = list(itertools.product(*list_of_appliances_centroids))
    sum_combination = np.array(np.zeros(len(states_combination)))
    for i in range(0, len(states_combination)):
        sum_combination[i] = sum(states_combination[i])
    length_sequence = len(df_mains_test.Mains_1_Power.values)
    states = np.zeros(length_sequence)
    residual_power = np.zeros(length_sequence)
    for i in range(length_sequence):
        [states[i], residual_power[i]] = find_nearest(
            sum_combination, df_mains_test.Mains_1_Power.values[i])
    [case_3_mains_1_states, case_3_mains_1_power] = decode_co(
        length_sequence, centroids, appliance_list, states, residual_power)

    appliance_list = [
        appliance for appliance in centroids if loads_to_mains_mapping[appliance] == 2]
    list_of_appliances_centroids = [calib_centroids[appliance]
                                    for appliance in appliance_list]
    states_combination = list(itertools.product(*list_of_appliances_centroids))
    sum_combination = np.array(np.zeros(len(states_combination)))
    for i in range(0, len(states_combination)):
        sum_combination[i] = sum(states_combination[i])
    length_sequence = len(df_mains_test.Mains_1_Power.values)
    states = np.zeros(length_sequence)
    residual_power = np.zeros(length_sequence)
    for i in range(length_sequence):
        [states[i], residual_power[i]] = find_nearest(
            sum_combination, df_mains_test.Mains_2_Power.values[i])
    [case_3_mains_2_states, case_3_mains_2_power] = decode_co(
        length_sequence, centroids, appliance_list, states, residual_power)

    case_3_states = dict(case_3_mains_1_states.items()
                         + case_3_mains_2_states.items())
    case_3_power = dict(case_3_mains_1_power.items()
                        + case_3_mains_2_power.items())

    power_states_dict = {
        0: {'states': case_0_states, 'power': case_0_power},
        1: {'states': case_1_states, 'power': case_1_power},
        2: {'states': case_2_states, 'power': case_2_power},
        3: {'states': case_3_states, 'power': case_3_power}
    }

    return power_states_dict
