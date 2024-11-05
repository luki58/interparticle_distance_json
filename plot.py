import json
import matplotlib.pyplot as plt
import numpy

# Load the data from the JSON file
file_path_20pa_t20 = 'VM1_AVI_230125_104431_20pa_t12/velocities.npy'
file_path_20pa_t30 = 'VM1_AVI_230125_104518_20pa_t13/velocities.npy'
#
string_path_20pa_t20 = 'VM1_AVI_230125_104431_20pa_t12/percentages.npy'
string_path_20pa_t30 = 'VM1_AVI_230125_104518_20pa_t13/percentages.npy'

pixelsize = 0.0147
fps = 60
vel_20pa_t20 = numpy.multiply(numpy.load(file_path_20pa_t20)[50:530,0], pixelsize*fps)
vel_20pa_t30 = numpy.multiply(numpy.load(file_path_20pa_t30)[:,0], pixelsize*fps)
#
string_data_20pa_t20 = numpy.load(string_path_20pa_t20)[50:530,1]
string_data_20pa_t30 = numpy.load(string_path_20pa_t30)[:,1]
#
x_20pa_t20 = numpy.arange(len(vel_20pa_t20))
x_20pa_t30 = numpy.arange(len(vel_20pa_t30))
#
x_string_20pa_t20 = numpy.arange(len(string_data_20pa_t20))
x_string_20pa_t30 = numpy.arange(len(string_data_20pa_t30))

# Plot the data
plt.figure(figsize=(14, 7),dpi=600)
plt.plot(x_20pa_t20, vel_20pa_t20, label='Velocity - 60% DC', color='#48A2F1', marker='x')
plt.plot(x_20pa_t30, vel_20pa_t30, label='Velocity - 65% DC', color='#48A2F1', marker='o', mfc='w')
plt.plot(x_string_20pa_t20, string_data_20pa_t20, label='String - 60% DC', color='#D81B1B', marker='x')
plt.plot(x_string_20pa_t30, string_data_20pa_t30, label='String - 65% DC', color='#D81B1B', marker='o', mfc='w')
plt.xlabel('Image number [#]')
plt.ylabel('v [mm/s] & String [%]')
plt.legend()
#plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()
plt.show()
