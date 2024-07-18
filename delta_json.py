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
import matplotlib.pyplot as plt
import pims
import json
import os
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
    #
    coef = np.polyfit(x_data,y_data,3)
    poly1d_fn = np.poly1d(coef)             # poly1d_fn is now a function which takes in x and returns an estimate for y
    #
    #fig, ax = plt.subplots(dpi=600)
    #fig.set_size_inches(4, 3)
    #ax.plot(x_fit, poly1d_fn(x_fit), linestyle='solid', color='#00cc00', linewidth=.7)
    #
    return poly1d_fn(x)

def n_e_interpolation(x, I):
    A = [1.92, 2.75, 3.15, 4.01]
    B = [-0.38, -0.42, -0.34, 0.047]
    y_data = np.add(np.multiply(A,I),np.multiply(B,I**2))
    x_data = [20, 40, 60, 100]
    x_fit = np.linspace(15,30,100)
    #
    coef = np.polyfit(x_data,y_data,1)
    poly1d_fn = np.poly1d(coef)             # poly1d_fn is now a function which takes in x and returns an estimate for y
    #
    #fig, ax = plt.subplots(dpi=600)
    #fig.set_size_inches(4, 3)
    #ax.plot(x_fit, poly1d_fn(x_fit), linestyle='solid', color='#00cc00', linewidth=.7)
    #
    return poly1d_fn(x)

### --- Interparticle Distance Analysis --- ###

def interparticle_distance(x_coords, y_coords, iter_step_dr, sigma, pixelsize):
    #
    cart_coords = np.transpose(np.vstack((x_coords, y_coords)))
    #
    g_r3, radii3 = rdf(cart_coords, dr=iter_step_dr, parallel=False)
    #
    g_r3 = gaussian_filter1d(g_r3, sigma=sigma)
    #
    #PLOT
    fig,ax = plt.subplots(dpi=600)
    #
    ax.plot(radii3, g_r3)
    #
    #Axes
    plt.xlabel('x[Pixel]')
    plt.ylabel('g_r')
    #
    peak = np.where(g_r3 == np.amax(g_r3))
    #
    print(peak[:])
    #
    if len(peak[0]) != 0:
        result_in_px = radii3[peak[0]][0]
        result_in_mm = radii3[peak[0]][0] * pixelsize #mm
    else:
        result_in_mm = result_in_px = 0
    #
    #print("From " + str(len(x_coords)) + " detected particle")
    #print("Average interparticle distance = "+str(result_in_mm)+" mm")
    #
    print(result_in_px)
    #
    return result_in_px
#
#MAIN
#
data_dir = 'data/'
# List all files in the data directory
files_list = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
#
data = json.load(open(files_list[1]))
x_coords = list(data['x'].values())
y_coords = list(data['y'].values())
#
#PLOT
fig,ax = plt.subplots(dpi=600)
ax.scatter(x_coords,y_coords, marker='o', color='#000000', linewidth=1, s=3)
plt.show()
#
pixelsize = 0.0147  #mm
sigma = 2           #smooth-filter rdf sginal with gauss to clear up main peak
iter_step_dr = 0.95  #from experience (accuracy and computationsla time taken into account)
#
id_mm = interparticle_distance(x_coords, y_coords, iter_step_dr, sigma, pixelsize)*pixelsize #Wigner_seitz radius
delta = 3/(4*np.pi*((id_mm)/1.79)**3)
#
'''    Havnes Parameter  P  '''
a = (1.3/2) *10**(-6) #micrometer particle radius
p = 100 #Pressure in Pascal
I = 1   #Current in mA
T_e = T_e_interpolation(p,I)
z = 0.3 #=0.3 +-0.1 for neon; Antonova
Z_d = 4*pi*epsilon_0*k*T_e*11600*a*z/(e**2)
n_e = n_e_interpolation(p, I)
n_d = delta**(-1/3)
'''    Ion number density    '''   
n_i0 = np.add(n_e, np.multiply(Z_d, n_d)) #m^-3 = n_e0 + Z_d*n_d ;melzer2019
P = np.multiply(np.multiply(695*(1.3/2),T_e),np.divide(n_d,n_i0))
print(P)