import pyvisa as visa
import pyperclip # Module to automatically save the temperature value to the clipboard
import time
import gc # Garbage Collection

while True:
    # Open an instance of the resource manager and assign the object handle rm
    rm = visa.ResourceManager()
    
    print(rm.list_resources()) # List available resources
    
    # Open an instance of the USB resource class and assign the task handle mm1
    mm1 =  rm.open_resource('USB0::0x05E6::0x2100::1270013::INSTR') 
    mm1.timeout = None # No timeout
    mm1.write('SAMPle:COUNt 1')
    
    
    r = mm1.query('MEAS:RES? 10000, MIN') # Resistance measurement in a 10 kOhm range and minimum resolution
     # All other commands are in the remote interface operations section of the manual
        
    #print(f'The resistance is {r} Ohms.')
    
    # Determining the temperature of the sample
    ref_resistance = 1 # in kOhms
    grad = 3850e-6 # Characteristic curve value in ppm/K
    r = float(r)/1000 # Resistance in kOhms
    
    delta_r = r - ref_resistance # Resistance measurement
    delta_t = (delta_r/grad) + 273.15 # Temperature of sample in Kelvin
    
    print('')
    print(f'The temperature is {delta_t} K.')
    print('')
    pyperclip.copy(delta_t) # Copying the temperature to the clipboard
    
    # Successfully clears and closes the program for the next measurement
    mm1.clear()
    mm1.close()
    rm.close()
    
    del delta_t # Clearing the delta_t value from memory
    del r  # Clearing the r value from memory
    del delta_r  # Clearing the delta_r value from memory
    gc.collect()
    
    time.sleep(6)    