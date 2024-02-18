############################################ 
###  
###   READ ME BEFORE USING
###   1. pip install pyserial
###   2. Connect Ardunio to PC
###   3. Open Device Manager
###   4. Under Ports (COM & LPT) find Arduino Uno
###   5. Assign COM value for variable ARDUINO_COM_PORT
###
############################################

import serial
import csv
import time
import os
import struct
import numpy

ARDUINO_COM_PORT = 'COM4'

### Note: Script WILL overwrite existing .csv file! Save accordingly!
# Change csv_dir_path to directory path of the CSV file
csv_dir_path = os.path.dirname(os.path.realpath(__file__))
# Change csv_file_name to desired file name
csv_file_name = 'csvfile.csv'
csv_file_path = os.path.join(csv_dir_path, csv_file_name)

arduino_serial = serial.Serial(ARDUINO_COM_PORT, 9600, parity='N', rtscts=False, xonxoff=False, timeout = 0.2)

def debug_read_print_line():
    while True:
        line = arduino_serial.readline().decode("utf-8").strip()
        print(line)

## WIP - Intepreted from legacy code - not tested.
def collect_data():
    writer = ''
    dat_list = bytearray()
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        while True:
            line = arduino_serial.readline()
            scan = 1
            if line == b'DAT\r\n':
                ndata = arduino_serial.read(4)
                num_points = struct.unpack("i",str(ndata))[0]
                ndata = ""
                num_read = 0
                doneReading = False
                while not doneReading:
                    pts_to_acquire = num_points*2 - num_read
                    if pts_to_acquire > 10000: #this is about 0.5 sec.
                        pts_to_acquire = 10000
                    new_dat = arduino_serial.read(pts_to_acquire)
                    dat_list.extend(new_dat)
                    this_num_read = len(new_dat)
                    num_read += this_num_read
                    if num_read == num_points*2:
                        doneReading = True
                fmt = str(len(dat_list)//2)+'h'
                adata = numpy.array(struct.unpack(fmt,str(dat_list)))
                write_to_file(adata, scan)
                scan += 1
                
## WIP - Intepreted from legacy code - not tested.
def write_to_file(adata, scan):
    fd = open(csv_file_path,'w')
    fd.write('#'+str(scan)+'\n')
    numpy.savetxt(fd, adata.astype(int), fmt='%d', newline='\n')
    fd.close()

if __name__ == '__main__':
    debug_read_print_line()
    # collect_data()