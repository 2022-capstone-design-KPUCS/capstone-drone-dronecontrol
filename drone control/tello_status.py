import socket
from time import sleep
import json

INTERVAL = 1

    
def tello_status():
    local_ip = ''
    local_port = 8890
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
    socket.bind((local_ip, local_port))

    tello_ip = '192.168.10.1'
    tello_port = 8889
    tello_adderss = (tello_ip, tello_port)

    socket.sendto('command'.encode('utf-8'), tello_adderss)

    try:
        index = 0
        while True:
            index += 1
            response, ip = socket.recvfrom(1024)
            if response == 'ok':
                continue
            data=response.decode('utf-8')
            out = data.replace(';', ' ')
            result=out.split()

            jsonString = json.dumps(result)
            print(jsonString)
            sleep(INTERVAL)
    except KeyboardInterrupt:
        pass