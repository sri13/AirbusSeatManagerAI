# -*- coding: utf-8 -*-
"""
Airline Seating Assignment Testing

How to execute: 
    python automatedTests.py

@authors: 
    Rohit Muthmare - 16201018
    Dinesh Kumar Sakthivel Pandi - 16200107 
    Srikanth Tiyyagura - 16203106
"""


import sys
sys.path.append("../")
import seat_assign_16201018_16200107_16203106


def automated_tests():
    '''
    >>> seat_assign_16201018_16200107_16203106.main()
    Error - Invalid Arguments Passed
    Correct Usage: python seat_assign_16201018__16200107_16203106.py *.db *.csv

    >>> sys.argv.append('database/Test_DB_1.db')
    >>> sys.argv.append('test_cases/Test_Case_1.csv')
    >>> seat_assign_16201018_16200107_16203106.main()
    Passegners refused :  0
    Passengers separated:  0
    Thank you for Booking with UCD Airlines.!
    
    >>> sys.argv[1]='database/Test_DB_2.db'
    >>> sys.argv[2]='test_cases/Test_Case_2.csv'
    >>> seat_assign_16201018_16200107_16203106.main()
    IO Error occured - test_cases\Test_Case_2.csv file not available.
    
    '''     
    return
    

    
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)