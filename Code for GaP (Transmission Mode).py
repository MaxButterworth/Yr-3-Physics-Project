import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import numpy as np
import math

data = pd.read_csv('GaP_Trans_2nd_Repeat_CSV.csv') # Open the spectrum csv file
data = data.to_numpy() # Convert data to a numpy array
wavelength = data[0:, 0] # Separating the 00 repeat of wavelength (in nm)
transmission = 0.01 * data[0:, 1] # Separating the 00 repeat of transmission and converting to a decimal
 
# Setting up arrays for non-negative values of transmission
T_filter=[]
wave_filter=[]
   
for i in range (1,len(transmission)): # Iteration over all elements
    if transmission[i] > 0: # Removes all negative transmissions
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
    alpha[j] = - (1/x) * math.log((((1 - R)**4 + (4 * T_filter[j] * T_filter[j] * R * R))**0.5 - (1 - R)**2)/(2 * T_filter[j] * R**2))

# Converting wavelength to energy in eV
E = np.zeros(len(wave_filter))
for k in range(0, len(wave_filter)):
    E[k] = ((6.626e-34 * 299792458)/np.array(wave_filter[k] * 1e-9)) / 1.602e-19
    
# Filter out negative alpha values
alpha_filter = []
E_filter = []
for z in range (1,len(alpha)): # Iteration over all elements
    if alpha[z] > 0: # Removes all negative alpha values
        alpha_filter.append(alpha[z])
        E_filter.append(E[z])

alpha_filter = np.array(alpha_filter)
E_filter = np.array(E_filter)

# Fit parameters for alpha^0.5 vs E
gradient_alpha = 4.001e1
y_intercept_alpha = -8.656e1
alpha_alpha_a = alpha_filter - ((gradient_alpha * E_filter) - y_intercept_alpha)

# Fit parameters for (alpha - alpha_a)^0.5 vs E
a_aa_grad = 7.937e+01
a_aa_yint = -1.760e+02

# Filter out negative alpha - alpha_a values
alpha_alpha_a_filter = []
E_alpha_a_filter = []
for y in range (1, len(alpha_alpha_a)): # Iteration over all elements
    if alpha_filter[y] > 0: # Removes all negative alpha - alpha_a values
        alpha_alpha_a_filter.append(alpha_filter[y])
        E_alpha_a_filter.append(E[y])
        
alpha_alpha_a_filter = np.array(alpha_alpha_a_filter)
E_alpha_a_filter = np.array(E_alpha_a_filter)

# Saving alpha_filter^0.5 and E data to csv
alpha_E = tuple(zip(E_filter, (alpha_filter**0.5))) # E is the first column
np.savetxt('alpha^0.5 vs E Data.csv', alpha_E, delimiter=',')

# Saving (alpha - alpha_a)^0.5 and E data to csv
alpha_E = tuple(zip(E_alpha_a_filter, (alpha_alpha_a_filter**0.5))) # E is the first column
np.savetxt('(alpha - alpha_a)^0.5 vs E Data.csv', alpha_E, delimiter=',')

# Set up the figure and axes for plotting
plt.rcParams.update({'font.size': 18}) # Sets the font size of all text to 12
plt.rcParams.update({"figure.facecolor": "white"}) # Sets the background colour of plot as white
plt.rcParams['axes.autolimit_mode'] = 'data' # Change data to data if you want round numbers at edges
plt.rcParams["figure.autolayout"] = True
fig1 = plt.figure(figsize = (14, 10))
fig2 = plt.figure(figsize = (14, 10))
fig3 = plt.figure(figsize = (14, 10))
fig4 = plt.figure(figsize = (14, 10))

# Setting up axes for original spectrum
ax1 = fig1.add_subplot(1, 1, 1)
ax1.set_xlabel('Wavelength (nm)')
ax1.set_ylabel('Transmission')
#ax1.set_title('Original Transmission Spectrum')
ax1.set_xlim(500, 600)
ax1.set_ylim(0, 0.6)

# Setting up axes for alpha
ax2 = fig2.add_subplot(1, 1, 1)
ax2.set_xlabel('Wavelength (nm)')
ax2.set_ylabel('Transmission (%)')
# ax2.set_title('Smoothed Transmission Spectrum')
ax2.set_xlim(500, 600)
ax2.set_ylim(0, 1)

# Setting up axes for alpha^0.5 vs E
ax3 = fig3.add_subplot(1, 1, 1)
ax3.set_xlabel('Energy (eV)')
ax3.set_ylabel('$\u03b1^{1/2}$ (cm)$^{-1}$')
#ax3.set_title('$\u03b1$ vs. $E$')
ax3.set_xlim(2, 2.5)
ax3.set_ylim(0, 12)

# Setting up axes for (alpha - alpha_a)^1/2 vs E
ax4 = fig4.add_subplot(1, 1, 1)
ax4.set_xlabel('Energy (eV)')
ax4.set_ylabel('$(\u03b1 - \u03b1_a)^{1/2}$ (cm)$^{-1}$')
ax4.set_xlim(2, 2.5)
ax4.set_ylim(0, 12)

# Plotting the data
ax1.plot(wave_filter, T_filter, linewidth=3) # Original spectrum
fig1.savefig('GaP Transmission Spectrum (Repeat 2).png', dpi=300, edgecolor='black')

ax2.plot(wave_filter, T_smooth, linewidth=3) # Smoothed spectrum
#fig2.savefig('GaP Smoothed Transmission Spectrum 295 K.png', dpi=300, edgecolor='black')

ax3.plot(E_filter, (alpha_filter)**0.5, linewidth=3) # alpha^1/2 vs E (eV)
ax3.plot(E_filter, ((gradient_alpha * E_filter) + y_intercept_alpha), linewidth=3) # Plotting linear fit
fig3.savefig('GaP Transmission Mode - alpha^0.5 vs E.png', dpi=300, edgecolor='black')

ax4.plot(E_alpha_a_filter, (alpha_alpha_a_filter)**0.5, linewidth=3) # (alpha - alpha_a)^1/2 vs E (eV)
ax4.plot(E_filter, ((a_aa_grad * E_filter) + a_aa_yint), linewidth=3) # Plotting linear fit
fig4.savefig('GaP Transmission Mode - (alpha - alpha_a)^0.5 vs E.png', dpi=300, edgecolor='black')

# Displaying the overall plots
plt.tight_layout()

plt.show()

print(-y_intercept_alpha/gradient_alpha) # E_g - E_p
print(-a_aa_yint/a_aa_grad) # E_g + E_p
print(((-y_intercept_alpha/gradient_alpha)+(-a_aa_yint/a_aa_grad))/2) # E_g