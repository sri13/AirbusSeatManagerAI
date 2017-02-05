# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 16:26:41 2017

@author: legend
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import sqlite3
import sys



# Reservation-Related Queries
def print_data_from_seating(c):
    for row in c.execute('SELECT * FROM seating'):
        print(row)
    
    
#Airbus seat Layout
def get_airbus_seat_layout(total_rows=15, total_seats=4):
    airbus_seat_layout = np.zeros((total_rows,total_seats),dtype=np.int)
    return airbus_seat_layout    


# Passenger-Related Queries

      
# Functions for validation
def read_csv(filename):
    bookings_temp_df=pd.read_csv(filename, names=['booking_name','booking_count'])
    return bookings_temp_df
    #bookings_df= pd.read_csv(filename)


def allocate_seats():
    return True

def check_empty_seats():
    return True
    
# main function to make call to all functions
if __name__ == "__main__":
    database_name= "airline_seating.db" #sys.argv[1]
    filename="bookings.csv"  #sys.argv[2]
    
# SQL connections.
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
#    print_data_from_seating(c)
   
    #Create airbus layout in memory 
    airbus_seat_layout=get_airbus_seat_layout()
    #print(airbus_seat_layout)
    
    #Import bookings.CSV file
    bookings_df=read_csv(filename)
    for each_booking in bookings_df:
        print(each_booking)
    
    
    
    