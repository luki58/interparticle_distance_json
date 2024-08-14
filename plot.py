import json
import matplotlib.pyplot as plt
import numpy

# Load the data from the JSON file
file_path_20pa = 'npy_data/VM2_AVI_230125_104901_20pa_t13/VM2_AVI_230125_104901_20pa_t13_results.json'
file_path_25pa = 'npy_data/VM2_AVI_230125_111238_25pa_t13/VM2_AVI_230125_111238_25pa_t13_results.json'
file_path_30pa = 'npy_data/VM2_AVI_230125_110058_30pa_t14/VM2_AVI_230125_110058_30pa_t14_results.json'
#
string_path_20pa = 'npy_data/VM2_AVI_230125_104901_20pa_t13/percentages.npy'
string_path_25pa = 'npy_data/VM2_AVI_230125_111238_25pa_t13/percentages.npy'
string_path_30pa = 'npy_data/VM2_AVI_230125_110058_30pa_t14/percentages.npy'

with open(file_path_20pa, 'r') as file:
    data_20pa = json.load(file)
with open(file_path_25pa, 'r') as file:
    data_25pa = json.load(file)
with open(file_path_30pa, 'r') as file:
    data_30pa = json.load(file)
#
string_data_20pa = numpy.load(string_path_20pa)
string_data_25pa = numpy.load(string_path_25pa)
string_data_30pa = numpy.load(string_path_30pa)

# Convert the data into a more usable format
data_20pa = {k: v for d in data_20pa for k, v in d.items()}
data_25pa = {k: v for d in data_25pa for k, v in d.items()}
data_30pa = {k: v for d in data_30pa for k, v in d.items()}

# Sort the data by image name
sorted_data_20pa = sorted(data_20pa.items())
sorted_data_25pa = sorted(data_25pa.items())
sorted_data_30pa = sorted(data_30pa.items())

# Extract the image names and distances
images_20pa, distances_20pa = zip(*sorted_data_20pa[30:-1])
images_25pa, distances_25pa = zip(*sorted_data_25pa[:-1])
images_30pa, distances_30pa = zip(*sorted_data_30pa[6:-1])

#
x_20pa = numpy.arange(len(images_20pa))
x_25pa = numpy.arange(len(images_25pa))
x_30pa = numpy.arange(len(images_30pa))

# Calculate number density n_d [m^-3]
pack_value = 1.79
nd_20pa_average = 3 / (4 * numpy.pi * ((numpy.average(distances_20pa)) *10**(-3) / pack_value)**3) * 10**(-10)
nd_25pa_average = 3 / (4 * numpy.pi * ((numpy.average(distances_25pa)) *10**(-3) / pack_value)**3) * 10**(-10)
nd_30pa_average = 3 / (4 * numpy.pi * ((numpy.average(distances_30pa)) *10**(-3) / pack_value)**3) * 10**(-10)
string_20pa_average = numpy.average(string_data_20pa[:,1])
string_25pa_average = numpy.average(string_data_25pa[:,1])
string_30pa_average = numpy.average(string_data_30pa[:,1])

# Plot the data
plt.figure(figsize=(14, 7))
plt.plot(x_20pa, distances_20pa, label='20 Pa', marker='o')
plt.plot(x_25pa, distances_25pa, label='25 Pa', marker='o')
plt.plot(x_30pa, distances_30pa, label='30 Pa', marker='o')
plt.xlabel('Image')
plt.ylabel('Average Interparticle Distance (mm)')
plt.legend()
#plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot the data
plt.figure(figsize=(14, 7))
plt.plot(numpy.arange(len(string_data_20pa[:,0])), string_data_20pa[:,1], label='20 Pa', marker='o')
plt.plot(numpy.arange(len(string_data_25pa[:,0])), string_data_25pa[:,1], label='25 Pa', marker='o')
plt.plot(numpy.arange(len(string_data_30pa[:,0])), string_data_30pa[:,1], label='30 Pa', marker='o')
plt.xlabel('Images')
plt.ylabel('String formation (%)')
plt.legend()
#plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot the data
plt.figure(figsize=(8, 5), dpi=400)
plt.plot(20, nd_20pa_average, label='20 Pa - $n_d \cdot 10^{10} m^{-3}$', marker='o', color='#D81B1B')
plt.plot(25, nd_25pa_average, label='25 Pa - $n_d \cdot 10^{10} m^{-3}$', marker='o', color='#D81B1B')
plt.plot(30, nd_30pa_average, label='30 Pa - $n_d \cdot 10^{10} m^{-3}$', marker='o', color='#D81B1B')
plt.plot(20, string_20pa_average, label='20 Pa - Strings DC65%', marker='d', color='#48A2F1')
plt.plot(25, string_25pa_average, label='25 Pa - Strings DC65%', marker='d', color='#48A2F1')
plt.plot(30, string_30pa_average, label='30 Pa - Strings DC70%', marker='d', color='#48A2F1')
plt.xlabel('Pressure (Pa)')
plt.ylabel('$n_d \cdot 10^{10} m^{-3}$ / String formation (%)')
plt.legend()
#plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()
plt.show()