import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

straight_line = pd.read_excel('Linear Fit Parameters (GaP).xlsx') # Open the linear parameters excel file
straight_line = straight_line.to_numpy() # Convert linear parameters to a numpy array

temp = straight_line[8, 1:]  # Separating the 00 repeat of temperature (in K)
Eg_wavelength = straight_line[4, 1:] # Wavelength corresponding to band gap energy

Eg = (6.626e-34 * 2.998e8)/(1.602e-19 * 1e-9 * Eg_wavelength) # Band gap energy in eV
Eg_error = straight_line[13, 1:] # Error on band gap measurements in eV

# Set up the figure and axes for plotting
plt.rcParams.update({'font.size': 18}) # Sets the font size of all text to 20
plt.rcParams.update({"figure.facecolor": "white"}) # Sets the background colour of plot as white
plt.rcParams['axes.autolimit_mode'] = 'data' # Change data to data if you want round numbers at edges
plt.figure(figsize = (14, 10))

# Setting up the axes
ax1 = plt.axes()
ax1.set_xlabel('Temperature (K)')
ax1.set_ylabel('$E_g$ (eV)')

# Plotting the sepctrum data
ax1.scatter(temp, Eg, s=70)
ax1.errorbar(temp, Eg, xerr=None, yerr=Eg_error, capsize=7, color='red', fmt='None')
ax1.plot(temp, (2.34 - ((6e-4*temp*temp)/(temp + 460))), linewidth=3, color='green', label='Varshni’s Equation for GaP') # Theoretical band gap vs temp relationship for GaP
#ax1.set_ylim(ymin=0)

# Displaying the overall plot
plt.tight_layout()
plt.savefig('Eg vs T Plot for GaP.png', dpi=300, edgecolor='auto')
plt.show()

print(np.average(Eg - (2.34 - ((6e-4*temp*temp)/(temp + 460))))) # Average difference between theory and experiment
print((np.std(Eg - (2.34 - ((6e-4*temp*temp)/(temp + 460)))))/np.sqrt(len(temp))) # Std error on the average
