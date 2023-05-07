import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np

data = pd.read_csv('GaAs_Full_Data_Trans.csv') # Open the spectrum csv file
data = data.to_numpy() # Convert data to a numpy array
wavelength = data[0:, 0] # Separating the 00 repeat of wavelength (in nm)
transmission = data[0:, 1] # Separating the 00 repeat of intensity
filtertrans=([])        #setting up arrays for non negative values
filterwave=([])
   
for k in range (1,len(transmission)):       #iteration over all elements
    if transmission[k] > 0:     #removes all negative transmissions
        filtertrans.append(transmission[k])
        filterwave.append(wavelength[k])           
  
# Smoothing the transmission data
""""filtertrans = savgol_filter(filtertrans, 101, 3)"""""

a=0.507182135
b=0.71216721
c=0.02436721
alpha=np.zeros(len(filtertrans))
for j in range(1, len(filtertrans)):        #iterates through alpha formula
     alpha[j]=-2325.58*math.log(((((a)+4*filtertrans[j]*filtertrans[j]*c)**0.5)-b)/2*filtertrans[j]*c)
   
energy=np.zeros(len(filterwave))        #wavelength to energy conversion
for p in range(1,len(filterwave)):
    energy[p]=(6.626e-34*299792458)/np.array(filterwave[p]*1e-9)
  
alphahv=alpha*energy
alphahvsquared=np.square(alphahv)       #alpha times energy squared
energy=energy/1.6e-19       #energy in eV
  
# Remove the (0,0) point from energy and alphashvquared graph
energy = energy[1:]
alphahvsquared = alphahvsquared[1:]
alpha_sq = (alpha[1:])**2

# create a dataframe with the variables
df = pd.DataFrame({'a': energy, 'b': alpha_sq})

# export the dataframe to a csv file for cftool
"df.to_csv('MLB Test Output (GaAs).csv', index=False)"

#linear fit parameters of linear portion (errors from CFTool)
# grad = 3.662e+10 ± 9.991e+09
# y-int = -5.103e+10 ± 1.400e+10

grad = 4.943e+10
y_int = -6.894e+10

# Set up the figure and axes for plotting
plt.rcParams.update({'font.size': 12}) # Sets the font size of all text to 20
plt.rcParams.update({"figure.facecolor": "white"}) # Sets the background colour of plot as white
plt.rcParams['axes.autolimit_mode'] = 'data' # Change data to data if you want round numbers at edges
fig1 = plt.figure(figsize = (14, 10))
fig2 = plt.figure(figsize = (14, 10))

# T vs Wavelength Spectrum
ax1 = fig1.add_subplot(1, 1, 1)
ax1.set_xlabel('Wavelength (nm)')
ax1.set_ylabel('Transmission (%)')

ax1.plot(wavelength, transmission, label='Spectrum') # Plotting the sepctrum data and linear fit
ax1.set_xlim((840, 950))
ax1.set_ylim((0, 100))

fig1.savefig('T vs Wavelength and Linear Fit for GaAs (Transmission at RTP) (Repeat 00).png', dpi=300, edgecolor='black')

# Alpha^2 vs E Plot
ax2 = fig2.add_subplot(1, 1, 1)
ax2.set_xlabel('Energy (eV)')
ax2.set_ylabel('$\u03b1^2$ (cm)$^{-1}$')

ax2.scatter(energy, alpha_sq, label='Spectrum') # Plotting the graoh
ax2.plot(energy, ((grad * energy) + y_int), label='Linear Fit', color='orange') # Plotting the linear fit
ax2.set_xlim((1.39, 1.42))
ax2.set_ylim((0, 1e9))

fig2.savefig('Alpha^2 vs E (Transmission at RTP) (Repeat 00).png', dpi=300, edgecolor='black')

plt.tight_layout()
plt.show()
    
    