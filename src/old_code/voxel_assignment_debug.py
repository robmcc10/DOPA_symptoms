#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 13:15:09 2017

@author: robmcc
"""
from configparser import ConfigParser
import glob
import nibabel as nib
import numpy as np
import pandas as pd
from json import loads
import sys


# NB node_ids are indexed from 0, but network ids start from 1
# Load directory and file ids
parser = ConfigParser()
#parser.read('/home/k1201869/DOPA_symptoms/src/project_details.txt')
parser.read('/Users/robmcc/mnt/droplet/home/k1201869/DOPA_symptoms/src/project_details_debug.txt')
main_directory = parser.get('project_details', 'main_directory')
beta_directory = parser.get('project_details', 'beta_directory')
roi_directory = parser.get('project_details', 'roi_directory')
voxel_maps_dir = ('%sresults/voxel_assigned_maps' % main_directory)
node_id_file = parser.get('project_details', 'node_id_file')
striatum_file = parser.get('project_details', 'striatum_file')
num_networks = int(parser.get('project_details', 'num_networks'))
num_top_seeds = int(parser.get('project_details', 'num_top_seeds'))
img_dim = (loads(parser.get("project_details", "image_dimension")))
img_dim = [int(i)for i in img_dim]

subject_id = sys.argv[1]

xvoxels = range(0, img_dim[0])
yvoxels = range(0, img_dim[1])
zvoxels = range(0, img_dim[2])


# functions


def network_shape(vector):
    """get node ids etc in correct shape"""
    a = np.array(vector)
    b = np.tile(a, (img_dim[0], img_dim[1], img_dim[2], 1))
    return np.transpose(b)


def assign_voxels(beta_maps):
    """assign each voxel to the network it
    has the most consistent connectivity to"""
    voxel_assignment = np.empty([img_dim[0], img_dim[1], img_dim[2]])
    for x in xvoxels:
        for y in yvoxels:
            for z in zvoxels:
                top_indices = np.empty([num_top_seeds, img_dim[0], img_dim[1], img_dim[2]])

                # the indices of nodes with greatest connectivity to the voxel:
                top_indices = np.argsort(-betas[:, x, y, z])[:num_top_seeds]

                # connectivity values of these nodes:
                top_betas = betas[top_indices, x, y, z]

                # the network these nodes belong too - in same order:
                top_network_nodes = np.array([node_details[i] for i in top_indices])
                top_combined = np.transpose(np.vstack([top_betas, top_network_nodes]))

                # empty array to be filled in below for loop
                mean_network_connectivity = np.zeros([2, num_networks])
                mean_network_connectivity[0, :] = range(1, num_networks+1)

                for network in range(1, num_networks+1):
                    # betas for single network:
                    individual_network = top_combined[top_combined[:, 1] == network]

                    # calculate the mean connectivity value for each of the networks:
                    mean_network_connectivity[1, (network-1)] = np.mean(individual_network[:, 0])

                # voxel_assignment = np.empty([img_dim[0], img_dim[1], img_dim[2]])

                # the network with greatest mean connectivity:
                voxel_assignment[x, y, z] = 1 + np.nanargmax(mean_network_connectivity[1, :])
    return voxel_assignment


# Node id dictionary
node_details = pd.read_excel((roi_directory + node_id_file))
node_details = node_details.set_index('node')['network'].to_dict()
node_ids = network_shape(node_details.keys())
network_ids = network_shape(node_details.values())

# all beta files for subject. File list runs through subject ids submitted by queue script
filelist = sorted(glob.glob('%(1)s/BETA_Subject%(2)s*.nii' % {"1": beta_directory, "2": '001'}))
betas = np.array([np.array((nib.load(fname, mmap=False)).get_data()) for fname in filelist])

# voxel_assignment
voxel_assignment = assign_voxels(betas2)
#np.save('%(1)s/voxel_assignment_%(2)s.npy' % {"1": voxel_maps_dir, "2": subject_id}, voxel_assignment)

betas2 = betas[0:50, :, :, :]
voxel_assignment.shape
voxel_assignment[45,40,40]

betas2.shape


betas[0,90,40,40]


x=41
y=40
z=40
top_indices = np.empty([num_top_seeds, img_dim[0], img_dim[1], img_dim[2]])

# the indices of nodes with greatest connectivity to the voxel:
top_indices = np.argsort(-betas[:, x, y, z])[:num_top_seeds]

# connectivity values of these nodes:
top_betas = betas[top_indices, x, y, z]

# the network these nodes belong too - in same order:
top_network_nodes = np.array([node_details[i] for i in top_indices])

top_combined = np.transpose(np.vstack([top_betas, top_network_nodes]))
top_combined

# empty array to be filled in below for loop
mean_network_connectivity = np.zeros([2, num_networks])
mean_network_connectivity[0, :] = range(1, num_networks+1)
mean_network_connectivity
for network in range(1, num_networks+1):
    # betas for single network:
    individual_network = top_combined[top_combined[:, 1] == network]

    # calculate the mean connectivity value for each of the networks:
    mean_network_connectivity[1, (network-1)] = np.mean(individual_network[:, 0])

voxel_assignment2 = np.empty([img_dim[0], img_dim[1], img_dim[2]])

# the network with greatest mean connectivity:
voxel_assignment2[x, y, z] = 1 + np.nanargmax(mean_network_connectivity[1, :])
voxel_assignment2[x, y, z]
