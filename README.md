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
