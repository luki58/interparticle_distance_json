# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 14:57:41 2024

@author: Lukas Wimmer
"""

from __future__ import division, unicode_literals, print_function  # for compatibility with Python 2 and 3

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import json
from rdfpy import rdf
from scipy.ndimage import gaussian_filter1d

# change the following to %matplotlib notebook for interactive plotting
# %matplotlib inline

# Optionally, tweak styles.
mpl.rc('figure', figsize=(10, 5))
mpl.rc('image', cmap='gray')

# Function to load coordinate data from JSON files in a folder
def load_coordinates_from_json(folder_path):
    coordinates = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    if 'x' in data and 'y' in data:
                        if isinstance(data['x'], list) and isinstance(data['y'], list):
                            coords = np.column_stack((data['x'], data['y']))
                            coordinates.append(coords)
                        else:
                            raise ValueError("JSON keys 'x' and 'y' must be lists.")
                    else:
                        raise KeyError("JSON must contain 'x' and 'y' keys with lists of coordinates.")
            except (ValueError, KeyError) as e:
                print(f"Error in file {filename}: {e}")
    return coordinates

# Function to compute the average interparticle distance
def average_interparticle_distance(coords, iter_step_dr, sigma, pixelsize):
    g_r, radii = rdf(coords, dr=iter_step_dr, parallel=False)
    g_r = gaussian_filter1d(g_r, sigma=sigma)
    
    fig, ax = plt.subplots(dpi=150)
    ax.plot(radii, g_r)
    plt.xlabel('x[Pixel]')
    plt.ylabel('g_r')
    plt.show()
    
    peak_index = np.argmax(g_r)
    average_distance_in_px = radii[peak_index]
    average_distance_in_mm = average_distance_in_px * pixelsize
    
    return average_distance_in_mm

# Main script
data_dir = 'json_data/'
coordinates = load_coordinates_from_json(data_dir)
frame_list = os.listdir(data_dir)

results = []
image = 0

for coords in coordinates:
    fig, ax = plt.subplots(dpi=200)
    ax.scatter(coords[:, 0], coords[:, 1], marker='o', color='#000000', linewidth=1, s=3)
    plt.show()

    pixelsize = 0.0118  # mm
    sigma = 2  # smooth-filter rdf signal with gauss to clear up main peak
    iter_step_dr = 1  # from experience (accuracy and computational time taken into account)

    avg_distance_mm = average_interparticle_distance(coords, iter_step_dr, sigma, pixelsize)
    
    nd = (avg_distance_mm * 1000) ** (-3)
    
    frame_description = frame_list[image].rstrip('.json')

    results.append({frame_description: nd})
    image += 1

# Save results to a JSON file
results_filename = os.path.basename(data_dir.rstrip('/')) + '_results.json'
results_filepath = os.path.join(data_dir, results_filename)

with open(results_filepath, 'w') as results_file:
    json.dump(results, results_file, indent=4)
    

