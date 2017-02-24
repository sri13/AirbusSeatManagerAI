-------------------------------------------------Airline_Seating_Arrangement----------------------------------------------------
                                        
                                          MIS40750: Analytics Research & Implementation

Name of the Contributors & Student ID

Srikanth Tiyyagura (16203106)

Dinesh Kumar Sakthivel Pandi (16200107)

Rohit Muthmare (16201018)

 Initial Conditions / Assumptions:

·  A Database file contains details on the layout of the plane along with the seat map. The plane may / may not have  previously booked seats.

·  A CSV file containing the number of bookings to be done.

·  Whenever a booking is accommodated, seats should be allocated together if possible, but split up if necessary.

·  When a booking cannot be accommodated at all, due to less free seats, seats should not be allocated.

·  On successful booking, booking details should be updated to the database after each booking request

·  The database should be updated with number of seats separated while booking and the number of bookings refused.

 

Implementation:

·  For allocating seats to the passengers, the seat map in the database file is replicated to a matrix format in memory.

·  For every booking, the matrix is checked for the availability of seats rather than checking the database file.

·  To minimize matrix search operations, first column of the matrix is used as counter of number of seats available in that row.

·  Before each booking request, number of seats to be booked is compared with total available seats in the plane to take booking decision.

·  After every successful booking, the database and the matrix is updated with the details of the passenger for  all bookings under that request.

·  If passengers must be separated, then the booking is traversed through each row and column until each group member has been given a seat.

·  The program is designed to allocate seats as a group wherever possible and seats separated value is considered based on the groups separated from each other, rather than individual persons.

·  At end of all booking requests, the database is updated with the number of passengers/ passenger groups separated and number of passengers refused.

 

Exception Handling:

·  Exceptions are the common scenarios that encounter very frequently and unknowingly, so these must be handled by all programs.

·  Try and Except blocks have been used to handle errors in all stages of program execution i.e. during input processing, files availability, database connections and reading / writing values to database.

·  Special care has been taken care to handle bad data scenarios like null values in the data and extra columns.

·  Database connection issues are quite common and steps has been taken to check database and individual tables availability.

 

Testing:

·  Functional Testing was done to check proper functioning of the code as expected.

·  Acceptance testing was done by providing proper input to the system to check for its working nature and then tested with all edge cases.

·  Negative Testing was also performed to check for the worst case scenarios in the system. In this case, parameters like negative and empty values in the booking are tested to check for the proper working of code.

·  Automated test cases has been created to use it in future in case of any changes to the application.

·  Complete test cases and scenario details available under testing folder.

 

Conclusion:

·  The submitted program works fine and has been rigorously tested with various scenarios.

·  The final code will demonstrate our collaboration and team work during the project.  

·  Updates were made wherever possible to enhance performance and optimise number of lines of code.

·  Future enhancements have been thought of identifying passenger uniquely and eliminate duplicates in the booking request file and handling special requirements of passengers.
