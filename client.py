import socket
import urllib.request
import json
import datetime
from common import *


err_number = 0
prev_time = ""
log_file = open(CLIENT_LOG_FILE, 'a')

while True:

    try:
        # keep parsing data
        req = urllib.request.Request(SOURCE_URL)
        response = urllib.request.urlopen(req)
        data = response.read(600000)
        
        err_number = 0
        # here json is stored as string
        my_json = data.decode('utf-8').replace("'", '"')

        # converting string to dictionary
        my_dict = json.loads(my_json)

        # getting the latest data
        latest_data = my_dict["records"][-1]

        # timestamp of latest data
        curr_time = latest_data["created"]

        if prev_time != curr_time:
            prev_time = curr_time
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((IP, PORT))
            client.send(json.dumps(latest_data).encode('utf-8'))
            client.close()
    except Exception as e:
        error_time = str(datetime.datetime.today().replace(microsecond=0))
        log_file.write(error_time + ' An exceptional thing happed - ' + str(e) + '\n')
        log_file.write(error_time + ' Some data might be missed in your DB\n')
        log_file.flush()
        err_number += 1
        if err_number == THRESHOLD_ERROR_LIMIT: 
            # consequtive errors crossed the threshold limit of errors
            log_file.write(error_time + ' Repeated errors, closing the client\n')
            log_file.flush()
            break



log_file.close()
client.close()
