# sheru-tezz-case-study
Case Study given by Sheru Tezz

This is the solution to the case study given as a part of recruitment test of Sheru Tezz.

This contains of three different files:

1. `common.py`: This file contains the common variables used by `server.py` and `client.py`
2. `server.py`: This file contains the server side code. The code starts a server at `127.0.0.1`, port `8081` and listens for connection. It creates a new database and whenever new data comes from client side, it adds the data in the table. Also, whenever there is any abnormality in the data (e.g.- battery percentage low), alert messages are shown. The error logs are stored in `serverErrorLogs.txt`.
4. `client.py`: This file contains the client side code. The client side code keeps looking at url given, whenever there is a new data point, the client connects to the server and sends the data to the server. The connection closes after the transfer of data. The client side error logs are stored in `clientErrorLog.txt`

For making the whole program fault tolerant, `try-except` statements are used.

Use `requirements.txt` for installing the requirements of the program.

To run the program, open two terminals and run the client and server programs in them separately.
```
python server.py // To run the server
python client.py // To run the client
```

I have completed all the tasks 1-4.

For task 5, the current code just prints out alerts to the terminal. To create a webpage I could have used HTML with Javascript, where Javascript would be used to accommodate the dynamic parts of the webpage. For generating the alerts for the webpage, I could have had create a flask server and which would figure out that whenever there is a new entry in the database which is according to the given conditions, the new server could send this information to the dynamic part, i.e. Javascript part of the webpage, which would then generate an alert.

For task 6, I could have created a simple webpage with a button redirecting to a Javascript code that would call the API for switching off the machine.
