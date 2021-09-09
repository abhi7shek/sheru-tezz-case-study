import socket
import json
import sqlite3
import datetime

from common import *

prevRecTime = [datetime.datetime.today().replace(microsecond=0)]*3
errno = 0

# Use this for physical database
dbconn = sqlite3.connect('iotdata.db')
# Use this for faster memory access
# dbconn = sqlite3.connect(':memory:')

dbconn.execute('''CREATE TABLE IF NOT EXISTS IOT_DATA
         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
         DEVICEIMEI     STRING    NOT NULL,
         LATITUDE       FLOAT     NOT NULL,
         LONGITUDE      FLOAT     NOT NULL,
         CELL1          FLOAT     NOT NULL,
         CELL2          FLOAT     NOT NULL,
         CELL3          FLOAT     NOT NULL,
         CELL4          FLOAT     NOT NULL,
         CELL5          FLOAT     NOT NULL,
         CELL6          FLOAT     NOT NULL,
         CELL7          FLOAT     NOT NULL,
         CELL8          FLOAT     NOT NULL,
         CELL9          FLOAT     NOT NULL,
         CELL10         FLOAT     NOT NULL,
         CELL11         FLOAT     NOT NULL,
         CELL12         FLOAT     NOT NULL,
         CELL13         FLOAT     NOT NULL,
         CELL14         FLOAT     NOT NULL,
         AVGCELL        FLOAT     NOT NULL,
         PACK           FLOAT     NOT NULL,
         CURRENT        FLOAT     NOT NULL,
         SOC            INTEGER   NOT NULL,
         CREATEDTIME    DATETIME  NOT NULL,
         RECIEVEDTIME   DATETIME  NOT NULL);''')

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((IP, PORT))
serv.listen(5)

while True:
    try:
        errno = 0
        conn, addr = serv.accept()
        data1 = conn.recv(3000)
        conn.close()
        data = json.loads(data1.decode('utf-8'))
        tdata = data['tdata'].split(',')
        print(tdata)
        dbconn.execute("INSERT INTO IOT_DATA (DEVICEIMEI, LATITUDE ,LONGITUDE, CELL1, CELL2, CELL3,\
            CELL4, CELL5, CELL6, CELL7, CELL8, CELL9, CELL10, CELL11, CELL12, CELL13, CELL14, AVGCELL,\
            PACK, CURRENT, SOC, CREATEDTIME, RECIEVEDTIME)\
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (tdata[0], float(tdata[1]),\
            float(tdata[2]), float(tdata[3]), float(tdata[4]), float(tdata[5]), float(tdata[6]), float(tdata[7]),\
            float(tdata[8]), float(tdata[9]), float(tdata[10]), float(tdata[11]), float(tdata[12]), float(tdata[13]),\
            float(tdata[14]), float(tdata[15]), float(tdata[16]), float(tdata[17]), float(tdata[18]), float(tdata[19]),\
            int(tdata[20]), data['created'], datetime.datetime.today().replace(microsecond=0)));
        dbconn.commit()
        cur = dbconn.cursor()
        # print(prevRecTime)
        query0 = "SELECT SOC,RECIEVEDTIME FROM IOT_DATA WHERE RECIEVEDTIME > DATETIME('" + str(prevRecTime[0]) + "') AND SOC < 20;"
        print(query0)
        cur.execute(query0)
        rows0 = cur.fetchall()
        if len(rows0)>0:
            print('Warning: Battery is', rows0[0][0],'at', rows0[0][1]) 
            prevRecTime[0] = datetime.datetime.strptime(rows0[0][1],'%Y-%m-%d %H:%M:%S')

        query1 = "SELECT PACK,RECIEVEDTIME FROM IOT_DATA WHERE RECIEVEDTIME > DATETIME('" + str(prevRecTime[1]) + "') AND PACK > 100;";
        cur.execute(query1)
        rows1 = cur.fetchall()
        if len(rows1)>0:
            print('Warning: Pack Voltage is', rows1[0][0],'at', rows1[0][1])  
            prevRecTime[1] = datetime.datetime.strptime(rows1[0][1],'%Y-%m-%d %H:%M:%S')
        
        query2 = "SELECT CURRENT,RECIEVEDTIME FROM IOT_DATA WHERE RECIEVEDTIME > DATETIME('" + str(prevRecTime[1]) + "') AND CURRENT < 0;";

        cur.execute(query2)
        rows2 = cur.fetchall()
        
        if len(rows2)>0:  
            print('Warning: Battery is discharging at', rows2[0][1])  
            prevRecTime[2] = datetime.datetime.strptime(rows2[0][1],'%Y-%m-%d %H:%M:%S')

    except Exception as e:
        print('Some data might be missed')
        print(e)
        errno += 1
        if errno == THRESHOLD_ERROR_LIMIT: 
            print('Repeated Errors')
            break

dbconn.close()
