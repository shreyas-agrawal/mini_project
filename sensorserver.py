"""Sensor servers

The sensors are connected to this node. It will collect data and send them
to the appropriate node for processing.
"""

import socket
import threading
import sys
import time
import os
import json
from imagedht import ImageDHT
from exttoip import ExtToIP
from updatelist import UpdateList


class SensorServer(threading.Thread):

    def __init__(self, connection, sensorAddress):

        threading.Thread.__init__(self)
        self.conn = connection
        self.sensorAddress = sensorAddress

    def run(self):

        (ipOfSensor, port) = self.sensorAddress
        data = self.conn.recv(50)
        decoded_data = json.loads(data.decode())
        print(decoded_data)
        worker_ip = ExtToIP(dht, decoded_data).getbest()
        print("work", worker_ip)
        worker_port = 10002
        worker_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        worker_sock.connect((worker_ip, worker_port))
        worker_sock.sendall(data)
        retanswer = worker_sock.recv(50)
        print(retanswer)
        # SEND DATA TO SENSOR


class Updateload():

    def __init__(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    @staticmethod
    def run():
        while True:
            cpu_avg = os.getloadavg()[0]
            dht.ip_to_cpu[sys.argv[1]] = cpu_avg
            time.sleep(5)


if __name__ == "__main__":

    if(len(sys.argv) < 2):
        print("usage: " + sys.argv[0] + " %ip [port] [seedip seedport]")
        sys.exit(2)

    ipaddress = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 12550
    seeed = tuple([sys.argv[3], int(sys.argv[4])]) if len(sys.argv) > 4 else ()
    dht = ImageDHT(ipaddress, port, seeed)
    UpdateList(dht, ipaddress)
    Updateload()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', 10005)
    sock.bind(server_address)
    sock.listen(10)

    while True:
        connection, sensorAddress = sock.accept()
        thread = SensorServer(connection, sensorAddress)
        thread.start()
