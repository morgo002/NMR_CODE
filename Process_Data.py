import pandas as pd
import numpy as np
from scipy.fft import fft
import matplotlib.pyplot as plt
import serial
import csv
import time
import os
import struct

ARDUINO_COM_PORT = 'COM4'

### Note: Script WILL overwrite existing .csv file! Save accordingly!
# Change csv_dir_path to directory path of the CSV file
csv_dir_path = os.path.dirname(os.path.realpath(__file__))
# Change csv_file_name to desired file name
csv_file_name = 'csvfile.csv'
csv_file_path = os.path.join(csv_dir_path, csv_file_name)



def debug_read_print_line():
    while True:
        line = arduino_serial.readline().decode("utf-8").strip()
        print(line)
        
## WIP - Intepreted from legacy code - not tested.
def write_to_file(adata, scan):
    fd = open(csv_file_path,'w')
    fd.write('#'+str(scan)+'\n')
    np.savetxt(fd, adata.astype(int), fmt='%d', newline='\n')
    fd.close()

def read_arduino(arduino_serial):
        '''
        Reads serial port, waiting for header signifying data transmission
        Return an int array of the data points.
        If first line read is not the data header, return None.
        '''
        chunk_size = 10000

        # Continually wait for arduino to transmit b'DAT/r/n' to indicate data transmission
        line = arduino_serial.readline()
        if line == b'DAT\r\n':
            # Unpack header containing number of bytes in message
            ndata = arduino_serial.read(4) 
            num_bytes_to_receive = struct.unpack("i",str(ndata))[0]

            bytes_left = num_bytes_to_receive

            # read buffer into dat_list
            data_bytes = bytearray()
            while(bytes_left > 0):
                if bytes_left-chunk_size > 0:
                    read_size = chunk_size
                else:
                    read_size = bytes_left
                new_data = arduino_serial.read(read_size)
                data_bytes.extend(new_data)

                bytes_left -= read_size    
            

            # format = '#h' with # as the number of two-byte short ints
            format = str(len(data_bytes)//2)+'h'
            # convert bytes to an array
            # struct.unpack() returns tuple of all data points
            return np.array(struct.unpack(format,str(data_bytes)))

        else: # Transmission was not data
            return None




if __name__ == "__main__":
    arduino_serial = serial.Serial(ARDUINO_COM_PORT, 9600, parity='N', rtscts=False, xonxoff=False, timeout = 0.2)    

    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)

        while True:
            # Continually wait for arduino to transmit b'DAT/r/n' to indicate data transmission
            data = read_arduino(arduino_serial)

            spectrum = fft(data)
            


            
            # # format = '#h' with # as the number of two-byte short ints
            # format = str(len(dat_list)//2)+'h'
            # # convert bytes to an array
            # # struct.unpack() returns tuple of all data points
            # adata = np.array(struct.unpack(format,str(dat_list)))
            # write_to_file(adata, scan)



    
