# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 20:44:47 2013

@author: nipun
"""

from sklearn import metrics
from sklearn.cluster import KMeans
import numpy as np
import random


def transform_data(df_appliances_train):
    raw_data = {}
    for key in df_appliances_train:
        data_gt_10 = df_appliances_train[key][df_appliances_train[key]>10].values
        raw_data[key] = data_gt_10[np.random.randint(0, len(data_gt_10), len(data_gt_10)/10)]
        length = len(raw_data[key])
        print length, key
        raw_data[key] = raw_data[key].reshape(length, 1)
    return raw_data


def apply_kmeans(X):
    '''Finds whether 2 or 3 gives better Silhouellete coefficient
    Whichever is higher serves as the number of clusters for that
    appliance'''
    num_clus = -1
    sh = -1
    k_means_labels = {}
    k_means_cluster_centers = {}
    k_means_labels_unique = {}
    for n_clusters in range(2, 3):
        k_means = KMeans(init='k-means++', n_clusters=n_clusters, n_jobs = -1, n_init=8)
        k_means.fit(X)
        k_means_labels[n_clusters] = k_means.labels_
        k_means_cluster_centers[n_clusters] = k_means.cluster_centers_
        k_means_labels_unique[n_clusters] = np.unique(k_means_labels)
        sh_n=metrics.silhouette_score(X, k_means_labels[n_clusters], metric='euclidean')
        if sh_n>sh:
            sh=sh_n
            num_clus=n_clusters


    return [num_clus + 1, k_means_labels[num_clus], k_means_cluster_centers[num_clus],  k_means_labels_unique[num_clus]]


def return_centroids_labels(df_appliances_train):
    transformed_data=transform_data(df_appliances_train)

    centroids = {}
    labels_appliance={}
    for appliance in df_appliances_train:
        print appliance
        [num_clus, labels, cluster_centers, labels_unique]=apply_kmeans(transformed_data[appliance])
        flattened=cluster_centers.flatten()
        sorted_list=np.sort(flattened)
        centroids[appliance]=sorted_list
        labels_=[]
        for label in labels:
            labels_.append(sorted_list.tolist().index(flattened[label]))
            labels_appliance[appliance]=np.array(labels_)
    for appliance in centroids:
        centroids[appliance]=list(np.array(centroids[appliance]).astype(int))
        centroids[appliance].sort()
    return [centroids,labels_appliance]



