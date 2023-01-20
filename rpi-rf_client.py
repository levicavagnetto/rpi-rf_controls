# @Author - Levi Cavagnetto
# Sends a message containing the value of the rf device to activate
# each number (1-3) is mapped to a specific 7 digit number, which 
# corresponds to either an off or on signal for a specific rf outlet
# receiver
import socket
import sys

unit = sys.argv[1]
status = sys.argv[2]

map_on = {"1": "2046460", "2": "2046458", "3": "2046457"}
map_off = {"1": "2046452", "2": "2046450", "3": "2046449"}

tcp_socket = socket.create_connection(('127.0.0.1', 1081))

data = ""
for x in unit:
    if status == "On":
        data += map_on[x] + ","
    elif status == "Off":
        data += map_off[x] + ","
try:
    data = data[:-1]
    print(data)
    tcp_socket.sendall(data.encode())
finally:
    print('Closing socket')
    tcp_socket.close()

