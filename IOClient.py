import socket
import time
import sys
import random
from simple_chalk import greenBright, redBright, blueBright, cyanBright
import databaseAlchemy as database
from setting import server_host, server_port

HOST = server_host
PORT = server_port

location_str = "|||||"
count = 0
weight = 5
moveOrders = []
msgQueue = []


def sendMsg():
    while len(msgQueue) != 0:
        toSend = msgQueue.pop(0)
        s.send(toSend.encode())
        print(cyanBright('Replied With: ') + toSend)
        time.sleep(0.1)


def findStartIndex(bin_id, location_string):
    locations = location_string.split('|')
    index_count = 0
    for index in locations:
        if index == bin_id:
            return index_count
        index_count = index_count + 1


def findMoveableIndex(start, end, location_string):
    locations = location_string.split('|')
    while start != end:
        temporary_end = end
        cannot_move = False
        while start != temporary_end:
            if (locations[temporary_end] != ''):
                cannot_move = True
            temporary_end = temporary_end - 1
        if (cannot_move is True):
            end = end - 1
        else:
            return end
    return end


def request(request_str):
    request_info = request_str.split('|')
    locations = location_str.split('|')

    if(request_info[1] == 'D'):
        if (locations[int(request_info[0])] == ''):
            return True
        else:
            return False
    elif (request_info[1] == 'P'):
        if (locations[int(request_info[0])] == request_info[2]):
            return True
        else:
            return False


def update(bin_id, action):
    temp_str = ''
    location_list = location_str.split('|')
    if (action == 0 or action == 5):
        location_list[action] = bin_id
    for y in range(5):
        temp_str = temp_str + location_list[y]+'|'
    temp_str = temp_str + location_list[5]
    return temp_str


def move():
    location_list = location_str.split('|')
    loop_count = 0
    temp_str = location_str
    while True:
        index_changed = False
        for move in moveOrders:
            starting_index = findStartIndex(move[4], temp_str)
            available_index = findMoveableIndex(starting_index, move[3], temp_str)
            if (available_index != starting_index):
                location_list[available_index] = location_list[starting_index]
                location_list[starting_index] = ''
                temp_str = ''
                for y in range(5):
                    temp_str = temp_str + location_list[y]+'|'
                temp_str = temp_str + location_list[5]
                index_changed = True
                location_list = temp_str.split('|')
            if (available_index == move[3]):
                moveOrders.remove(move)
                time.sleep(0.1)
                reply_to_return = "ST,"+str(sys.argv[1])+",J,"+move[0]+","+str(move[2])+"|"+str(move[3])+"|"+move[1]+"|"+move[4]+";"
                msgQueue.append(reply_to_return)
                sendMsg()
                print("Finished Moving: "+reply_to_return)
        if (index_changed is False):
            break
        else:
            loop_count = loop_count + 1
    return temp_str


def reply_breakdown(reply):
    temp_str = ''
    temp_list = []
    location_list = reply.split('|')
    # Traverse location_list and move them over one location
    for x in range(6):
        if x == 0:
            temp_list.append(location_list[5])
        else:
            temp_list.append(location_list[x-1])
    # creating the reply string
    for y in range(5):
        temp_str = temp_str + temp_list[y]+'|'
    temp_str = temp_str + temp_list[5]
    return temp_str


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    reply_to_return = "ST,1"+",P,Pairing;"
    msgQueue.append(reply_to_return)
    sendMsg()
    while True:
        recievedData = False
        data = s.recv(1024)
        decoded_data = data.decode()
        split_data = decoded_data.split(',')
        print(blueBright("Received: ")+decoded_data)

        if (split_data[0] == "ACK"):
            print("The server has acknowledged message.")
        elif ("ROTATION" in decoded_data):
            # Breakdown, move position and remake string
            location_reply = reply_breakdown(location_str)
            location_str = location_reply  # Update location_str with new value
            msgQueue.append(reply_to_return)
            sendMsg()
            print(cyanBright("Replied with: " + reply_to_return))
        elif ("ST,1"+",S;" in decoded_data):
            reply_to_return = "ST,1"+",S,"+location_str+";"
            msgQueue.append(reply_to_return)
            sendMsg()
        elif ("ST,1"+",U" in decoded_data):
            reply_to_return = "ACK,"+decoded_data
            msgQueue.append(reply_to_return)
            sendMsg()
            decoded_data = decoded_data.replace(';', '')
            split_data = decoded_data.split(",")
            bin_info = split_data[4].split("|")
            if(bin_info[0] == "0"):
                update_str = update(bin_info[2], 0)
                location_str = update_str
            elif (bin_info[0] == "5"):
                update_str = update('', 5)
                location_str = update_str
                new_location = move()
                location_str = new_location
                time.sleep(0.1)
            reply_to_return = "ST,1"+",S,"+location_str+";"
            msgQueue.append(reply_to_return)
            sendMsg()

        elif ("ST,1"+",M" in decoded_data):
            reply_to_return = "ACK,"+decoded_data
            msgQueue.append(reply_to_return)
            sendMsg()
            decoded_data = decoded_data.replace(';', '')
            split_data = decoded_data.split(",")
            move_info = split_data[4].split("|")
            start_index = int(move_info[0])
            end_index = int(move_info[1])
            direction = move_info[2]
            moveOrders.append([split_data[3], direction, start_index, end_index, move_info[3]])
            new_location = move()
            location_str = new_location
            reply_to_return = "ST,"+str(sys.argv[1])+",S,"+location_str+";"
            msgQueue.append(reply_to_return)
            sendMsg()

        elif ("ST,1"+",R" in decoded_data):
            decoded_data = decoded_data.replace(';', '')
            split_data = decoded_data.split(',')
            check_request = request(split_data[4])
            if check_request is True:
                reply_to_return = "ST,1"+",A,1,"+split_data[4]+";"
                msgQueue.append(reply_to_return)
                sendMsg()
            else:
                reply_to_return = "ST,1"+",D,1,"+split_data[4]+";"
                msgQueue.append(reply_to_return)
                sendMsg()

        elif ("ST,1"+",W" in decoded_data):
            # decoded_data = decoded_data.replace(';', ',')
            # reply_to_return = decoded_data+str(weight)+";"
            # s.send(reply_to_return.encode())
            # print(cyanBright("Replied with: " + reply_to_return))
            # weight = weight+1

            decoded_data = decoded_data.replace(';', ',')
            print("decoded", decoded_data)
            

            reply_break_list = decoded_data.split(',')
            bin_id = reply_break_list[3]
            action = reply_break_list[4]
            print("bin_id is ", bin_id)
            print("action is ", action)
            check = database.findfakeBinExists(bin_id)

            print("check is", check)
            if check == 1:
                weight = 5
            else:
                random_no = random.randint(5, 6)
                if(action == "IN"):
                    weight = database.findfakeBinWeight(bin_id)+random_no
                if(action == "OUT"):
                    weight = database.findfakeBinWeight(bin_id)-random_no

            database.CreateUpdatefakeBinWeight(bin_id, weight, check)
            reply_to_return = decoded_data+str(weight)+";"
            # s.send(reply_to_return.encode())
            msgQueue.append(reply_to_return)
            sendMsg()
            print("Replied with: "+reply_to_return)
            print("weight", weight)
