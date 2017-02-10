# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 16:26:41 2017

@author: legend
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import sqlite3
import os.path
import sys


#global varibales
SQL_CURSR = None

#sql connection
def get_connection(database_name):
    conn = sqlite3.connect(database_name)
    global SQL_CURSR
    SQL_CURSR = conn.cursor()
    return 

def get_rows_cols():
    global SQL_CURSR
    for row in SQL_CURSR.execute("SELECT * FROM rows_cols"):
        print(row)
    return
    
def get_booked_seats():
    global SQL_CURSR
    for row in SQL_CURSR.execute("SELECT * FROM seating"):
        print(row)
    return
    
# Reservation-Related Queries
def get_metrics():
    global SQL_CURSR
    for row in SQL_CURSR.execute('SELECT * FROM metrics'):
        print(row)
    return
        

#Setup Environment 
def setup_airbus_layout(total_rows=15, total_seats=4):
    airbus_seat_layout = get_airbus_seat_layout(total_rows, total_seats)
    total_free_seats = np.sum(airbus_seat_layout[:,0])
    return airbus_seat_layout, total_free_seats
    
#Airbus seat Layout
def get_airbus_seat_layout(total_rows=15, total_seats=4):
    airbus_seat_layout = np.zeros((total_rows,total_seats+1),dtype=np.int)
    airbus_seat_layout[:,0] = total_seats
    return airbus_seat_layout    


    
    
# Passenger-Related Queries

      
# Functions for validation
def read_csv(filename):
    bookings_temp_df=pd.read_csv(filename, names=['booking_name','booking_count'])
    return bookings_temp_df
    #bookings_df= pd.read_csv(filename)


def allocate_seats(index, row, total_free_seats,airbus_seat_layout):
    booking_count = row['booking_count']

#    Allocations side by side
    for each_row in range(airbus_seat_layout.shape[0]):
        if(booking_count!=0 and airbus_seat_layout[each_row][0]>=booking_count):
            for each_column in range(airbus_seat_layout.shape[1]):
                if(airbus_seat_layout[each_row][each_column]==0):
                    airbus_seat_layout[each_row][each_column]=index
                    booking_count -=1
                    total_free_seats-=1
                    airbus_seat_layout[each_row][0]-=1
                if booking_count ==0:
#                    print(booking_count,total_free_seats,airbus_seat_layout[each_row][0])
                    break
#    No Allocation done and book separately
    if(booking_count == row['booking_count']):
        print(index,"Sidebyside not possible")
        for each_row in range(airbus_seat_layout.shape[0]):
            if(booking_count!=0 and airbus_seat_layout[each_row][0]!=0):
                for each_column in range(airbus_seat_layout.shape[1]):
                    if(airbus_seat_layout[each_row][each_column]==0):
                        airbus_seat_layout[each_row][each_column]=index
                        booking_count -=1
                        total_free_seats-=1
                        airbus_seat_layout[each_row][0]-=1
                    if booking_count ==0:
#                        print(booking_count,total_free_seats,airbus_seat_layout[each_row][0])
                        break
    
    return total_free_seats,airbus_seat_layout

def check_empty_seats():
    return True
    
# main function to make call to all functions
def main():
    
    #Input Processing from input file
    if(len(sys.argv) == 3):
        database_name= os.path.dirname(__file__) + "/../airline_seating.db" #sys.argv[1]
        filename=os.path.dirname(__file__) + "/../bookings.csv"  #sys.argv[2]
        
        get_connection(database_name)
        
        #    print_data_from_seating(c)
        get_booked_seats()
        
        get_rows_cols()
        
        get_metrics()
         
        #Create airbus layout in memory 
        airbus_seat_layout,total_free_seats=setup_airbus_layout()
#        print(airbus_seat_layout,total_free_seats)
            
        #Import bookings.CSV file
        bookings_df=read_csv(filename)
            
        for index,row in bookings_df.iterrows():
            if total_free_seats >= row['booking_count']:
    #            print(index+1, row['booking_name'], row['booking_count'])
                total_free_seats,airbus_seat_layout=allocate_seats(index+1,row,total_free_seats,airbus_seat_layout)
#                print(total_free_seats,airbus_seat_layout)
            else:
                print(index+1,row['booking_count'],"Seats not available to complete booking")
        
        print(airbus_seat_layout)
    
    else:
        print("Error - Invalid Arguments Passed")
        print("Correct Usage: python seat_assign_16201018__16200107_16203106.py *.db *.csv")
    
    return
    
    
if __name__ == "__main__":
    main()