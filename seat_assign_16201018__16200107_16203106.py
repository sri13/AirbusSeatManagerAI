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
    
    
    


# Passenger-Related Queries

      
# Functions for validation
def read_csv(filename):
    bookings_temp_df=pd.read_csv(filename)
    return bookings_temp_df
    #bookings_df= pd.read_csv(filename)


def allocate_seats():
    return True

def check_empty_seats():
    return True
    
# main function to make call to all functions
if __name__ == "__main__":
    database_name= sys.argv[1]
    filename=sys.argv[2]
    
# SQL connections.
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    print_data_from_seating(c)
    
# Import CSV
    bookings_df=read_csv(filename)
    
    print(bookings_df)
    
    
    
    