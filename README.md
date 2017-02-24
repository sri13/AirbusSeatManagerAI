-------------------------------------------------Airline_Seating_Arrangement----------------------------------------------------
                                        
                                          MIS40750: Analytics Research & Implementation

Name of the Contributors & Student ID

Srikanth Tiyyagura (16203106)

Dinesh Kumar Sakthivel Pandi (16200107)

Rohit Muthmare (16201018)

Initial Conditions(Assumptions):

* A Database file showing the layout of the plane along with the seat map. The plane might also contain some previously booked seats.

* A CSV file containing the number of bookings to be done.

* Whenever a booking is accommodated, seats should be allocated together if possible, but split up if necessary. 
  When a booking cannot be accommodated at all, due to less free seats, seats should not be allocated.

* The database should be updated with number of seats separated while booking and the number of bookings refused.

Implementation:

For allocating seats to the passengers, the seat map in the database file is replicated to a matrix format.
For every booking the matrix is checked for the availability of seats rather than checking the database file.
After every successful booking the database and the matrix is updated with the details of the passengers along with the number of bookings.
If passengers must be separated, then the booking is traversed through each row and column until each group member has been given a seat.
We try to allocate seats alongside the greatest number of passengers possible.
After every booking, the database is updated with the number of number of passengers separated and number of passengers refused.

Testing:

Initially, the code is testing is performed to check proper functioning of the code. Acceptance testing is done by providing proper input to the system to check for its working nature. Next is Functional Testing in which the components of the code are tested to check every functionality of the code.
Negative Testing is also performed to check for the worst case scenarios in the system.In this case, parameters like negative and empty values in the booking are tested to check for the proper working of code.

Conclusion:

The submitted program works fine and has been rigorously tested with various scenarios. The final code will demonstrate our collaboration and team work during the project. There are some updates made to optimise the code to satisfy the conditions given. 


