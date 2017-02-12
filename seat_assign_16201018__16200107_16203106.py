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
SQL_CONN = None
SQL_CURSR = None

PASSENGERS_REFUSED = 0
PASSENGERS_SEPARATED = 0

FLIGHT_NROWS = 0
FLIGHT_SEATS = ''


#sql connection
def get_connection(database_name):
    global SQL_CURSR, SQL_CONN
    SQL_CONN = sqlite3.connect(database_name)
    SQL_CURSR = SQL_CONN.cursor()
    return 

def get_rows_cols():
    global SQL_CURSR, FLIGHT_NROWS, FLIGHT_SEATS
    SQL_CURSR.execute("SELECT * FROM rows_cols")
    row = SQL_CURSR.fetchone()
    FLIGHT_NROWS = row[0]
    FLIGHT_SEATS = str(row[1])
#    print(FLIGHT_NROWS, ",", FLIGHT_SEATS, ",", len(FLIGHT_SEATS))
    return

def get_metrics():
    global SQL_CURSR, PASSENGERS_REFUSED, PASSENGERS_SEPARATED
    SQL_CURSR.execute('SELECT * FROM metrics')
    row = SQL_CURSR.fetchone()
    PASSENGERS_REFUSED = row[0]
    PASSENGERS_SEPARATED = row[1]
#    print(PASSENGERS_REFUSED, ",", PASSENGERS_SEPARATED)
    return
    
def get_booked_seats():
    global SQL_CURSR , SQL_CONN, FLIGHT_SEATS
    bookedSeatsList = []
    seat_cursr = SQL_CONN.cursor()
    SQL_CURSR.execute("SELECT name, count(1) FROM seating where name != '' " +\
                      " group by name")
    for row in SQL_CURSR.fetchall():
        seat_cursr.execute("SELECT row, seat from seating where name = '%s' " % row[0])
        seat = seat_cursr.fetchone()        
        for each_seat in range(row[1]):
            bookedSeatsList.append((seat[0]-1, FLIGHT_SEATS.index(seat[1])+1))
#    print(bookedSeatsList)
    return bookedSeatsList
    
def update_seat(booking_name, row_num, column_num):
    global SQL_CURSR, FLIGHT_SEATS
#    print(booking_name, row_num+1, FLIGHT_SEATS[column_num-1])
    SQL_CURSR.execute("update seating " + \
                      " set name = ? " + \
                      " where row = ? and seat = ? " \
                      , (booking_name, (row_num+1), FLIGHT_SEATS[column_num-1]))
    SQL_CONN.commit()
    return
    
def update_metrics():
    global SQL_CURSR, PASSENGERS_REFUSED, PASSENGERS_SEPARATED
    SQL_CURSR.execute("update metrics " + \
                      " set passengers_refused= ?, passengers_separated= ?" \
                      , (PASSENGERS_REFUSED, PASSENGERS_SEPARATED) )
    SQL_CONN.commit()
    return
        

#Setup Environment 
def setup_airbus_layout(total_rows=15, total_seats=4, bookedSeatsList=None ):
    airbus_seat_layout = get_airbus_seat_layout(total_rows, total_seats)
    total_free_seats = np.sum(airbus_seat_layout[:,0])
    for seat in bookedSeatsList:
#        print(seat)
        airbus_seat_layout[seat]= -1
        airbus_seat_layout[seat[0],0] -=1
        total_free_seats -= 1
#    print(airbus_seat_layout)
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
    global PASSENGERS_SEPARATED

#    Allocations side by side
    for each_row in range(airbus_seat_layout.shape[0]):
        if(booking_count!=0 and airbus_seat_layout[each_row][0]>=booking_count):
            for each_column in range(airbus_seat_layout.shape[1]):
                if(airbus_seat_layout[each_row][each_column]==0):
                    airbus_seat_layout[each_row][each_column]=index
                    booking_count -=1
                    total_free_seats-=1
                    airbus_seat_layout[each_row][0]-=1
                    update_seat(row['booking_name'],each_row,each_column)
                if booking_count ==0:
#                    print(booking_count,total_free_seats,airbus_seat_layout[each_row][0])
                    break
#    No Allocation done and book separately
    if(booking_count == row['booking_count']):
        print(index,"Sidebyside not possible")
        prev_row = 0
        for each_row in range(airbus_seat_layout.shape[0]):
            if(booking_count!=0 and airbus_seat_layout[each_row][0]!=0):
                for each_column in range(airbus_seat_layout.shape[1]):
                    if(airbus_seat_layout[each_row][each_column]==0):
                        # Determine where first row allocated
                        if(booking_count==row['booking_count']):
                            prev_row = each_row
                        
                        airbus_seat_layout[each_row][each_column]=index
                        booking_count -=1
                        total_free_seats-=1
                        airbus_seat_layout[each_row][0]-=1
                        update_seat(row['booking_name'],each_row,each_column)
                        
                        # if the seat allocated in a new row
                        if(prev_row != each_row):
                            PASSENGERS_SEPARATED += 1
                        
                    if booking_count ==0:
#                        print(booking_count,total_free_seats,airbus_seat_layout[each_row][0])
                        break
    
    return total_free_seats,airbus_seat_layout

    
# main function to make call to all functions
def main():
    
    #Input Processing from input file
    if(len(sys.argv) == 3):
        
        global PASSENGERS_REFUSED, PASSENGERS_SEPARATED
        
        database_name= os.path.dirname(__file__) + "/../airline_seating.db" #sys.argv[1]
        filename=os.path.dirname(__file__) + "/../bookings.csv"  #sys.argv[2]
        
        get_connection(database_name)
        
        # Load data from database 
        get_rows_cols()
        
        get_metrics()
        
        bookedSeatsList = get_booked_seats()
        
        global FLIGHT_NROWS, FLIGHT_SEATS         
        #Create airbus layout in memory 
        airbus_seat_layout,total_free_seats=setup_airbus_layout(FLIGHT_NROWS, \
                                        len(FLIGHT_SEATS), bookedSeatsList )
#        print(airbus_seat_layout,total_free_seats)
            
        #Import bookings.CSV file
        bookings_df=read_csv(filename)
            
        for index,row in bookings_df.iterrows():
            if total_free_seats >= row['booking_count']:
    #            print(index+1, row['booking_name'], row['booking_count'])
                total_free_seats,airbus_seat_layout=allocate_seats(index+1,row,total_free_seats,airbus_seat_layout)
#                print(total_free_seats,airbus_seat_layout)
            else:
#                print(index+1,row['booking_count'],"Seats not available to complete booking")
                PASSENGERS_REFUSED += 1
        
        print(airbus_seat_layout)
        update_metrics()
    
    else:
        print("Error - Invalid Arguments Passed")
        print("Correct Usage: python seat_assign_16201018__16200107_16203106.py *.db *.csv")
    
    return
    
    
if __name__ == "__main__":
    main()