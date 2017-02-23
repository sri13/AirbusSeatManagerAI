# -*- coding: utf-8 -*-
"""
Airline Seating Assignment 

@authors: 
    Rohit Muthmare - 16201018
    Dinesh Kumar Sakthivel Pandi - 16200107 
    Srikanth Tiyyagura - 16203106
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import sqlite3
import sys
from pathlib import Path

#Global Variables

#Variable for Database Connection is Initially declared as None(No Connection Initally)
SQL_CONN = None
#Variable for Executing the Query and storing it in Memory
SQL_CURSR = None

#Variable to store the number of passenger refused booking
PASSENGERS_REFUSED = 0
#Variable to store the number of passengers separated in a group booking
PASSENGERS_SEPARATED = 0

#Variable to get the seat configuration from the database
FLIGHT_NROWS = 0
FLIGHT_SEATS = ''



def get_connection(database_name):
    '''
    Function to establish connection to the database    
    '''    
    global SQL_CURSR, SQL_CONN        
    
    try:       
        #Passing Database name as an arguement to establish connection
        SQL_CONN = sqlite3.connect(database_name)   
        
        #Variable storing the Database cursor for future operations
        SQL_CURSR = SQL_CONN.cursor()
    
    except sqlite3.Error as e:
        print("Error during Database Connection - " + e.args)
        sys.exit(1) 
    return 



def get_rows_cols():
    '''
    Function to obtain the Seat configuration
    '''
    global SQL_CURSR, FLIGHT_NROWS, FLIGHT_SEATS
    
    try:
        #Fetching the seat configuration from the database 
        SQL_CURSR.execute("SELECT * FROM rows_cols")
        row = SQL_CURSR.fetchone()
        
        FLIGHT_NROWS = row[0]
        FLIGHT_SEATS = str(row[1])
        
    except sqlite3.Error as e:
            print("Error during Flight seat map config. retrival - " + e.args[0])
            sys.exit(1)
    return



def get_metrics():
    '''
    Function to obtain the Separated and Refused passengers
    '''
    global SQL_CURSR, PASSENGERS_REFUSED, PASSENGERS_SEPARATED
    
    try:
        #Fetching the value of number of passengers refused and number of passengers separated from the database
        SQL_CURSR.execute('SELECT * FROM metrics')
        row = SQL_CURSR.fetchone()
    
        PASSENGERS_REFUSED = row[0]
        PASSENGERS_SEPARATED = row[1]
    
    except sqlite3.Error as e:
            print("Error during Flight Metrics retrival - " + e.args[0])
            sys.exit(1)
    return



def get_booked_seats():
    '''
    Function to obtain the Previous bookings in the flight
    '''
    global SQL_CURSR , SQL_CONN, FLIGHT_SEATS
    bookedSeatsList = []

    try:
        seat_cursr = SQL_CONN.cursor()
        #Fetching the previously booked seats from the database
        SQL_CURSR.execute("SELECT name, count(1) FROM seating where name != '' " +\
                          " group by name")
        for row in SQL_CURSR.fetchall():
            #Fetching the row and set number of previous boking from database
            seat_cursr.execute("SELECT row, seat from seating where name = '%s' " % row[0])
            for each_seat in seat_cursr.fetchall():
                bookedSeatsList.append((each_seat[0]-1, FLIGHT_SEATS.index(each_seat[1])+1))
        
    except sqlite3.Error as e:
        print("Error during booked seats retrival - " + e.args[0])
        sys.exit(1)
    return bookedSeatsList



def update_seat(booking_name, row_num, column_num):
    '''
    Function to update the database with Bookings
    '''
    global SQL_CURSR, FLIGHT_SEATS
    
    try:
        #Update the seating table with name of the passenger and the seats allocated 
        SQL_CURSR.execute("update seating " + \
                          " set name = ? " + \
                          " where row = ? and seat = ? " \
                          , (booking_name, (row_num+1), FLIGHT_SEATS[column_num-1]))
        SQL_CONN.commit()
    
    except sqlite3.Error as e:
            print("Error in Updating Passenger Details- " + e.args[0])
            sys.exit(1)
    return



def update_metrics():
    '''
    Function to update the database with separated passengers
    and refused bookings
    '''
    global SQL_CURSR, PASSENGERS_REFUSED, PASSENGERS_SEPARATED
    
    try:
        #Update metrics table with number of passengers separated and count of bookings refused
        SQL_CURSR.execute("update metrics " + \
                          " set passengers_refused= ?, passengers_separated= ?" \
                          , (PASSENGERS_REFUSED, PASSENGERS_SEPARATED) )
        SQL_CONN.commit()
    
    except sqlite3.Error as e:
            print("Error in Updating Passenger Metrics - " + e.args[0])
            sys.exit(1) 
    return
        


def setup_airbus_layout(total_rows, total_seats, bookedSeatsList=None ):
    '''
    Setup Environment for Airbus
    '''
    if(total_rows >0 and total_seats > 0):
        airbus_seat_layout = get_airbus_seat_layout(total_rows, total_seats)
        total_free_seats = np.sum(airbus_seat_layout[:,0])
        for seat in bookedSeatsList:
            airbus_seat_layout[seat]= -1
            airbus_seat_layout[seat[0],0] -=1
            total_free_seats -= 1
        return airbus_seat_layout, total_free_seats
    else:
        print("Error in airbus layout : total rows - " + total_rows + \
              " total seats - " + total_seats)
        sys.exit(1)
 
    

def get_airbus_seat_layout(total_rows, total_seats):
    '''
    Function to setup Airbus seat Layout in memory
    checks done in parent function
    '''
    airbus_seat_layout = np.zeros((total_rows,total_seats+1),dtype=np.int)
    airbus_seat_layout[:,0] = total_seats
    return airbus_seat_layout    

      
def read_csv(filename):
    '''
    Function to fetch the booking details from csv file
    '''
    try:
        # names list help to read only two columns in the file
        bookings_temp_df=pd.read_csv(filename, names=['booking_name','booking_count']) 
        return bookings_temp_df
        
    except Exception as e:
        print("Unhandled exception occured on reading bookings file - " + e.args[0])
        sys.exit(1)
    
    

def allocate_seats(index, row, total_free_seats,airbus_seat_layout):
    '''
    Function to allocate seats for the bookings
    '''
    booking_count = row['booking_count']
    
    global PASSENGERS_SEPARATED, FLIGHT_SEATS

    try:
        #Allocations side by side
        for each_row in range(airbus_seat_layout.shape[0]):
            if( booking_count!=0 and ( (airbus_seat_layout[each_row][0]>=booking_count) \
                or ( (booking_count > len(FLIGHT_SEATS)) and \
                       (airbus_seat_layout[each_row][0] == len(FLIGHT_SEATS))))):
                for each_column in range(airbus_seat_layout.shape[1]):
                    if(airbus_seat_layout[each_row][each_column]==0):
                        airbus_seat_layout[each_row][each_column]=index
                        booking_count -=1
                        total_free_seats-=1
                        airbus_seat_layout[each_row][0]-=1
                        update_seat(row['booking_name'],each_row,each_column)
                    if booking_count ==0:
                        return total_free_seats,airbus_seat_layout
    
        #No Allocation done and book separately
        if(booking_count !=0):
            first_row = 0
            prev_row = 0
            for each_row in range(airbus_seat_layout.shape[0]):
                if(booking_count!=0 and airbus_seat_layout[each_row][0]!=0):
                    for each_column in range(airbus_seat_layout.shape[1]):
                        if(airbus_seat_layout[each_row][each_column]==0):
                            
                            #Identify row where first seat allocated
                            if(booking_count==row['booking_count']):
                                first_row = each_row
                                prev_row = each_row
                                
                            airbus_seat_layout[each_row][each_column]=index
                            booking_count -=1
                            total_free_seats-=1
                            airbus_seat_layout[each_row][0]-=1
                            update_seat(row['booking_name'],each_row,each_column)
                            
                            #If the seat is allocated in a new row and 
                            # not any bookings made on same row
                            if((first_row != each_row) and (prev_row != each_row)):
                                PASSENGERS_SEPARATED += 1
                                prev_row = each_row
                            
                        if booking_count ==0:
                            return total_free_seats,airbus_seat_layout
    except Exception as e:
         print("Error occured during allocation - " + e.args[0])
         sys.exit(1)
         return

def main():
    """
    Main function to invoke other functions to start booking process
    """    
    try:
        
        if(len(sys.argv) == 3):
            
            # load file names to global variables after doing basic checks
            global PASSENGERS_REFUSED, PASSENGERS_SEPARATED
            
            if(Path(sys.argv[1]).is_file()):
                database_name= sys.argv[1]
            else:
                raise IOError( sys.argv[1] + " file not available.")
        
            if(Path(sys.argv[2]).is_file()):
                filename= sys.argv[2]
            else:
                raise IOError( sys.argv[2] + " file not available.")
                
            #Establish connection to database name
            get_connection(database_name)
            
            #Load data from database to memory
            get_rows_cols()
            
            get_metrics()
            
            bookedSeatsList = get_booked_seats()
            
            #Create airbus layout in memory 
            global FLIGHT_NROWS, FLIGHT_SEATS         
            airbus_seat_layout,total_free_seats=setup_airbus_layout(FLIGHT_NROWS, \
                                            len(FLIGHT_SEATS), bookedSeatsList )
            
            #Import bookings.CSV file
            bookings_df=read_csv(filename)
            
            for index,row in bookings_df.iterrows():
                # if any of the rows contain bad data, then skip
                if(pd.isnull(row['booking_count']) or pd.isnull(row['booking_name']) \
                             or row['booking_count'] <=0):
                    print("Skipped Bad Data - ",row['booking_name'], row['booking_count'])
                    continue
                
                if total_free_seats >= row['booking_count']:
                    total_free_seats,airbus_seat_layout=allocate_seats(index+1, \
                                    row,total_free_seats,airbus_seat_layout)
                else:
        
                    PASSENGERS_REFUSED += int(row['booking_count'])

                # update metrics at the end
                update_metrics()
            
            #print metrics    
            print("Passegners refused : ",PASSENGERS_REFUSED )
            print("Passengers separated: ", PASSENGERS_SEPARATED)
            print("Thank you for Booking with UCD Airlines.!")
        
        else:
            print("Error - Invalid Arguments Passed")
            print("Correct Usage: python seat_assign_16201018__16200107_16203106.py *.db *.csv")

    except IOError as err:
        print("IO Error occured - "+ err.args[0])
    
    except Exception as err:
        print("Unknow Error occured in Main - ", err.args)
        
    return
    
    
if __name__ == "__main__":
    main()
