import socket
import time
import sys
from simple_chalk import greenBright, redBright, blueBright, cyanBright
from setting import server_host, server_port

from setting import server_host, server_port

HOST = server_host
PORT = server_port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send((str(sys.argv[1])+","+str(sys.argv[2])+",P,Pairing;").encode())

    while True:
        data = s.recv(1024)
        decoded_data = data.decode()
        split_data = decoded_data.split(',')
        print(blueBright("Received Message: ") + decoded_data)

        if (split_data[0] == "ACK"):
            print("The server has acknowledged message.")
        elif ("SUCCESS" in decoded_data):
            time.sleep(0.1)
            reply_to_return = str(sys.argv[1])+","+str(sys.argv[2])+",R;"
            s.send(reply_to_return.encode())
            print(cyanBright("Replied with: " + reply_to_return))
        elif (str(sys.argv[1])+","+str(sys.argv[2])+",R,QC;" in decoded_data):
            time.sleep(0.1)
            reply_to_return = "ACK," + decoded_data
            s.send(reply_to_return.encode())
            print(cyanBright("Replied with: " + reply_to_return))
        elif (str(sys.argv[1])+","+str(sys.argv[2])+",N,A" in decoded_data):
            time.sleep(0.1)
            reply_to_return = "ACK," + decoded_data
            s.send(reply_to_return.encode())
            print(cyanBright("Replied with: " + reply_to_return))

            time.sleep(0.1)
            reply_to_return = str(sys.argv[1]) + ","+str(sys.argv[2])+","+split_data[2] + "," + split_data[3] + ",JD," + split_data[4]
            s.send(reply_to_return.encode())
            print(cyanBright("Replied with: " + reply_to_return))
