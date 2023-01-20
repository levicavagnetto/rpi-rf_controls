# @Author - Levi Cavagnetto
# Sends a decimal code via a 433/315MHz GPIO device
# 'code', metavar='CODE', type=int, help="Decimal code to send"
# '-g', dest='gpio', type=int, default=17, help="GPIO pin (Default: 17)"
# '-p', dest='pulselength', type=int, default=None, help="Pulselength (Default: 350)"
# '-t', dest='protocol', type=int, default=None, help="Protocol (Default: 1)"
# '-l', dest='length', type=int, default=None, help="Codelength (Default: 24)"
# '-r', dest='repeat', type=int, default=10, help="Repeat cycles (Default: 10)"

import socket
import sys
import logging

from rpi_rf import RFDevice

logging.basicConfig(filename='rpi-rf/rpi-rf_console.log', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S', format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s',)

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('0.0.0.0', 1081)
tcp_socket.bind(server_address)

tcp_socket.listen(1)

while True:
    #print("Waiting for connection")
    connection, client = tcp_socket.accept()

    try:
        #print("Connected to client IP: {}".format(client))

        while True:
            data = connection.recv(128)
            if data:
                #print("Received data: {}".format(data.decode()))
                
                rfdevice = RFDevice(17)
                rfdevice.enable_tx()
                rfdevice.tx_repeat = 15
                            
                tx_codes = data.decode().split(',')
                for x in range(len(tx_codes)):
                    rfdevice.tx_code(int(tx_codes[x]), 1, 199, 24)
                    logging.info(tx_codes[x] + 
                                " [protocol: " + "1" + 
                                ", pulselength: " + "199" + 
                                ", length: " + "24(default)" + 
                                ", repeat: " + str(rfdevice.tx_repeat) + "]")

            elif not data:
                rfdevice.cleanup()
                break

    finally:
        connection.close()
