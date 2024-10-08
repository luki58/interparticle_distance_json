# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 14:57:41 2024

@author: Lukas Wimmer
"""

from __future__ import division, unicode_literals, print_function  # for compatibility with Python 2 and 3

import matplotlib as mpl
import matplotlib.pyplot as plt

# change the following to %matplotlib notebook for interactive plotting
#%matplotlib inline

# Optionally, tweak styles.
mpl.rc('figure',  figsize=(10, 5))
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
import scienceplots

### --- Te interpolation from Pustilnik (measured in absence of microparticles) --- ###

def T_e_interpolation(x, I):
    C = [7.13, 7.06, 6.98, 5.5]
    D = [1.23, 0.75, 0.77, 1.59]
    y_data = np.add(C,np.divide(D,I))
    x_data = [20, 40, 60, 100]
    x_fit = np.linspace(15,30,100)
    coef = np.polyfit(x_data,y_data,3)
    poly1d_fn = np.poly1d(coef)  # poly1d_fn is now a function which takes in x and returns an estimate for y
    return poly1d_fn(x)

def n_e_interpolation(x, I):
    A = [1.92, 2.75, 3.15, 4.01]
    B = [-0.38, -0.42, -0.34, 0.047]
    y_data = np.add(np.multiply(A,I),np.multiply(B,I**2))
    x_data = [20, 40, 60, 100]
    x_fit = np.linspace(15,30,100)
    coef = np.polyfit(x_data,y_data,1)
    poly1d_fn = np.poly1d(coef)  # poly1d_fn is now a function which takes in x and returns an estimate for y
    return poly1d_fn(x)

# Function to load numpy arrays from a folder
def load_numpy_arrays_from_folder(folder_path):
    numpy_arrays = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.npy'):
            file_path = os.path.join(folder_path, filename)
            numpy_array = np.load(file_path)
            numpy_arrays.append(numpy_array)
    return numpy_arrays

# Function to compute interparticle distance
def interparticle_distance(x_coords, y_coords, iter_step_dr, sigma, pixelsize):
    cart_coords = np.column_stack((x_coords, y_coords))
    g_r3, radii3 = rdf(cart_coords, dr=iter_step_dr, parallel=False)
    g_r3 = gaussian_filter1d(g_r3, sigma=sigma)
    fig,ax = plt.subplots(dpi=600)
    ax.plot(radii3, g_r3)
    plt.xlabel('x[Pixel]')
    plt.ylabel('g_r')
    peak = np.where(g_r3 == np.amax(g_r3))
    if len(peak[0]) != 0:
        result_in_px = radii3[peak[0]][0]
        result_in_mm = radii3[peak[0]][0] * pixelsize
    else:
        result_in_mm = result_in_px = 0
    return result_in_px

# Main script
data_dir = 'npy_data/VM2_AVI_230125_104901_20pa_t13'
numpy_arrays = load_numpy_arrays_from_folder(data_dir)

results = []

for array in numpy_arrays:
    x_coords = array[:, 0]
    y_coords = array[:, 1]

    fig,ax = plt.subplots(dpi=600)
    ax.scatter(x_coords, y_coords, marker='o', color='#000000', linewidth=1, s=3)
    plt.show()

    pixelsize = 0.0147  # mm
    sigma = 2  # smooth-filter rdf signal with gauss to clear up main peak
    iter_step_dr = 0.95  # from experience (accuracy and computational time taken into account)

    id_mm = interparticle_distance(x_coords, y_coords, iter_step_dr, sigma, pixelsize) * pixelsize
    delta = 3 / (4 * np.pi * ((id_mm) / 1.79)**3)
    
    results.append({
        'delta': delta
        })

# Save results to a JSON file
results_filename = os.path.basename(data_dir.rstrip('/')) + '_results.json'
results_filepath = os.path.join(data_dir, results_filename)

with open(results_filepath, 'w') as results_file:
    json.dump(results, results_file, indent=4)


