import pandas as pd
import matplotlib.pyplot as plt

straight_line = pd.read_excel('Linear Fit Parameters (GaP).xlsx') # Open the linear parameters excel file
straight_line = straight_line.to_numpy() # Convert linear parameters to a numpy array
j = 1 # Set counter to cycle through the linear parameters

for i in range(80, 310, 10):
    data = pd.read_csv('GaP_{}K_Full_Data.csv'.format(i)) # Open the spectrum csv file
        
    data = data.to_numpy() # Convert data to a numpy array
    
    wavelength = data[0:, 0] # Separating the 00 repeat of wavelength (in nm)
    intensity = data[0:, 1] # Separating the 00 repeat of intensity
    
    # Set up the figure and axes for plotting
    plt.rcParams.update({'font.size': 12}) # Sets the font size of all text to 20
    plt.rcParams.update({"figure.facecolor": "white"}) # Sets the background colour of plot as white
    plt.rcParams['axes.autolimit_mode'] = 'data' # Change data to data if you want round numbers at edges
    plt.figure(figsize = (14, 10))
    
    # Setting up the axes
    ax1 = plt.axes()
    ax1.set_xlabel('Wavelength (nm)')
    ax1.set_ylabel('Intensity (Counts)')
    
    # Plotting the sepctrum data
    ax1.plot(wavelength, intensity, label='Spectrum')
    
    # Getting relevant linear parameters to plot the straight line
    grad = straight_line[0, j]
    y_int = straight_line[2, j]
    
    # Plotting the straight line
    ax1.plot(wavelength, ((grad * wavelength) + y_int), label='Linear Fit')
    ax1.set_xlim(500, 650)
    ax1.set_ylim(0, 60000)
    
    # Displaying the overall plot
    plt.tight_layout()
    plt.savefig('Spectrum and Linear Plot for GaP at {} K (Repeat 00).png'.format(i), dpi=300, edgecolor='auto')
    plt.show()
    
    j += 1
    
    