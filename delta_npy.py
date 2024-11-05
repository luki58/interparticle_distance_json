# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 14:57:41 2024

@author: Lukas Wimmer
"""

from __future__ import division, unicode_literals, print_function  # for compatibility with Python 2 and 3

import matplotlib as mpl
import matplotlib.pyplot as plt

# change the following to %matplotlib notebook for interactive plotting
# %matplotlib inline

# Optionally, tweak styles.
mpl.rc('figure', figsize=(10, 5))
mpl.rc('image', cmap='gray')

import numpy as np
import os
import json
import trackpy as tp
from rdfpy import rdf
from scipy.optimize import curve_fit
import scipy.special as scsp
from scipy.ndimage import gaussian_filter, gaussian_filter1d
from scipy.constants import epsilon_0, k, pi, e

# Function to load numpy arrays from a folder
def load_numpy_arrays_from_folder(folder_path):
    numpy_arrays = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.npy'):
            file_path = os.path.join(folder_path, filename)
            numpy_array = np.load(file_path)
            numpy_arrays.append(numpy_array)
    return numpy_arrays

# Function to compute the average interparticle distance
def average_interparticle_distance(x_coords, y_coords, iter_step_dr, sigma, pixelsize):
    cart_coords = np.column_stack((x_coords, y_coords))
    g_r3, radii3 = rdf(cart_coords, dr=iter_step_dr, parallel=False)
    g_r3 = gaussian_filter1d(g_r3, sigma=sigma)
    
    fig, ax = plt.subplots(dpi=150)
    ax.plot(radii3, g_r3)
    plt.xlabel('x[Pixel]')
    plt.ylabel('g_r')
    plt.show()
    
    peak_index = np.argmax(g_r3)
    average_distance_in_px = radii3[peak_index]
    average_distance_in_mm = average_distance_in_px * pixelsize
    
    return average_distance_in_mm

# Main script
data_dir = 'npy_data/positions'
#data_dir = 'npy_data/VM2_AVI_230125_104901_20pa_t13'
#data_dir = 'npy_data/VM2_AVI_230125_111238_25pa_t13'
numpy_arrays = load_numpy_arrays_from_folder(data_dir)
frame_list = os.listdir(data_dir)

results = []
image = 0

for array in numpy_arrays:
    x_coords = array[:, 0]
    y_coords = array[:, 1]

    fig, ax = plt.subplots(dpi=200)
    ax.scatter(x_coords, y_coords, marker='o', color='#000000', linewidth=1, s=3)
    plt.show()

    pixelsize = 0.0147  # mm
    sigma = 2  # smooth-filter rdf signal with gauss to clear up main peak
    iter_step_dr = 1  # from experience (accuracy and computational time taken into account)

    avg_distance = average_interparticle_distance(x_coords, y_coords, iter_step_dr, sigma, pixelsize)
    print(frame_list[image][:-4] + " of " + str(len(numpy_arrays)) + " with average distance = " + str(avg_distance))

    results.append({
        frame_list[image][:-4]: avg_distance
    })
    image += 1
    
# Save results to a JSON file
results_filename = os.path.basename(data_dir.rstrip('/')) + '_results.json'
results_filepath = os.path.join(data_dir, results_filename)

with open(results_filepath, 'w') as results_file:
    json.dump(results, results_file, indent=4)
