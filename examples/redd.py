'''Peforms NILM analysis on REDD dataset

Usage: 
python redd.py location_of_home_in_redd output_file_name

eg. python /home/nipun/study/datasets/MIT/low_freq/house_1/ 1

This will store the results (Mean Normalized Error and RMS Error)
in 1.md, which is a markup output_file. You may then use any markup renderer
for pretty viewing of data

For exploratory analysis, it is recommended that you run the code in an IPython 
console (with pylab inline)

$ ipython --pylab inline

In [6]: run redd.py /home/nipun/study/datasets/MIT/low_freq/house_1/ 1

'''

from indic.load_data import load_mains_data
from indic.load_data import load_labels
from indic.load_data import load_appliances_data
from indic.downsample import downsample
from indic.align_mains_appliances import find_intersection
from indic.divide_test_train import partition_train_test
from indic.reject_insignificant_appliances import reject_insignificant_appliance
from indic.assign_load_to_mains import assign_load_to_mains
from indic.identify_clusters import return_centroids_labels
from indic.calibration import calibrate_centroids
from indic.co import apply_co
from indic.compute_results import compute_RE_MNE
from indic.plot_results import draw_table
import sys


# Path to a REDD home
path = sys.argv[1]

# Path to save the results
output_file = sys.argv[2]

print 'Loading Mains Data'
df_mains = load_mains_data(path)
labels = load_labels(path)
print 'Loading appliance Data'
df_appliances = load_appliances_data(path, labels)

# Downsampling
print 'Downsampling'
downsampling_window = '1Min'
df_mains_downsampled = downsample(df_mains, downsampling_window)
df_appliances_downsampled = downsample(df_appliances, downsampling_window)

print 'Aligning time series'
# Aligning mains and appliances time series
common_index = find_intersection(
    df_mains_downsampled, df_appliances_downsampled)
df_mains_downsampled_aligned = df_mains_downsampled.ix[common_index]
df_appliances_downsampled_aligned = df_appliances_downsampled.ix[common_index]

print 'Removing appliances'
# Removing appliances whose contribution is insignificant
df_appliances_downsampled_aligned_remove_insignificant = reject_insignificant_appliance(
    df_appliances_downsampled_aligned)

print 'Loads to mains_mapping'
# Loads to mains mapping
loads_to_mains_mapping = assign_load_to_mains(
    df_mains_downsampled_aligned, df_appliances_downsampled_aligned_remove_insignificant)

for app in df_appliances_downsampled_aligned_remove_insignificant:
    if app not in loads_to_mains_mapping:
        print "DELETING", app
        del df_appliances_downsampled_aligned_remove_insignificant[app]

print loads_to_mains_mapping

# Dividing the data into test and train
[df_train_mains, df_train_appliances, df_test_mains, df_test_appliances] = partition_train_test(
    df_mains_downsampled_aligned, df_appliances_downsampled_aligned_remove_insignificant)

print df_appliances_downsampled_aligned_remove_insignificant.describe()
print 'Clustering'
# Finding the centroids and labels assigned to the data
[centroids, labels] = return_centroids_labels(df_train_appliances)

# Finding the calibrated centroids
calib_centroids = calibrate_centroids(
    df_train_mains, df_train_appliances, labels, centroids, loads_to_mains_mapping)

print 'Performing CO'
# Peform CO
power_states_dict = apply_co(
    centroids, calib_centroids, loads_to_mains_mapping, df_test_mains)

# Compute results
[MNE, RE] = compute_RE_MNE(power_states_dict, df_test_appliances)

# Draw table
draw_table(MNE, RE, output_file)
