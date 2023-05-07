import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import numpy as np

data = pd.read_csv('GaP_Full_Data_Trans.csv') # Open the spectrum csv file
data = data.to_numpy() # Convert data to a numpy array
wavelength = data[0:, 0] # Separating the 00 repeat of wavelength (in nm)
transmission = 0.01 * data[0:, 1] # Separating the 00 repeat of transmission and converting to a decimal
 
# Setting up arrays for non-negative values of transmission
T_filter=[]
wave_filter=[]
   
for i in range (1,len(transmission)): # Iteration over all elements
    if transmission[i] >= 0: # Removes all negative transmissions
        T_filter.append(transmission[i])
        wave_filter.append(wavelength[i])    

# Smoothing the transmission data
T_smooth = savgol_filter(T_filter, 101, 3)

# Defining constants/values
T_alpha_0 = np.average(T_smooth[2271:2417]) # T at alpha = 0 to determine R (indices taken from wave_filter array)
R = (1 - T_alpha_0)/(1 + T_alpha_0)
x = 4.1e-2 # Thickness of the GaP sample in cm

# Determing alpha for each wavelength of filtered transmission data
alpha = np.zeros(len(T_filter))
for j in range(0, len(T_filter)):
    alpha[j] = - (1/x) * np.log(((((1 - R)**4 + (4 * T_filter[j]**2 * R**2))**0.5) - ((1 - R)**2)) / (2 * T_filter[j] * R**2))

# Converting wavelength to energy in eV
E = np.zeros(len(wave_filter))
for k in range(0, len(wave_filter)):
    E[k] = ((6.626e-34 * 299792458)/np.array(wave_filter[k] * 1e-9)) / 1.602e-19

# Saving alpha and E data to csv
alpha_E = tuple(zip(E, alpha)) # E is the first column
np.savetxt('alpha vs E data.csv', alpha_E, delimiter=',')

# Set up the figure and axes for plotting
plt.rcParams.update({'font.size': 24}) # Sets the font size of all text to 20
plt.rcParams.update({"figure.facecolor": "white"}) # Sets the background colour of plot as white
plt.rcParams['axes.autolimit_mode'] = 'data' # Change data to data if you want round numbers at edges
plt.rcParams["figure.autolayout"] = True
fig1 = plt.figure(figsize = (14, 10))
fig2 = plt.figure(figsize = (14, 10))
fig3 = plt.figure(figsize = (14, 10))

# Setting up axes for original spectrum
ax1 = fig1.add_subplot(1, 1, 1)
ax1.set_xlabel('Wavelength (nm)')
ax1.set_ylabel('Transmission')
#ax1.set_title('Original Transmission Spectrum')
ax1.set_xlim(850, max(wave_filter))
ax1.set_ylim(0, 1)

# Setting up axes for alpha
ax2 = fig2.add_subplot(1, 1, 1)
ax2.set_xlabel('Wavelength (nm)')
ax2.set_ylabel('Transmission')
#ax2.set_title('Smoothed Transmission Spectrum')
ax2.set_xlim(850, max(wave_filter))
ax2.set_ylim(0, 1)

# Setting up axes for alpha
ax3 = fig3.add_subplot(1, 1, 1)
ax3.set_xlabel('Energy (eV)')
ax3.set_ylabel('$\u03b1$ (cm)$^{-1}$')
#ax3.set_title('$\u03b1$ vs. $E$')
"""ax3.set_xlim(1.36, 1.4)
ax3.set_ylim(0, 13000)"""

# Plotting the data
ax1.plot(wave_filter, T_filter) # Original spectrum
#plt.savefig('GaP Transmission Spectrum 295 K.png', dpi=300, edgecolor='black')

ax2.plot(wave_filter, T_smooth) # Smoothed spectrum
#plt.savefig('GaP Smoothed Transmission Spectrum 295 K.png', dpi=300, edgecolor='black')

ax3.plot(E, (alpha)**0.5) # alpha vs E (eV)
#plt.savefig('GaP Transmission Mode - alpha vs E.png', dpi=300, edgecolor='black')

# Displaying the overall plots
plt.tight_layout()

plt.show()