import socket
import time
import sys
import random
from simple_chalk import greenBright, redBright, blueBright, cyanBright

import database
from setting import server_host, server_port

HOST = server_host  # Replace with Server IP
PORT = server_port

location_str = "||||||||"
count = 0
weight = 5
moveOrders = []


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
        if (int(request_info[0]) <= 5):
            if (locations[int(request_info[0])] == ''):
                return True
        elif (int(request_info[0]) > 5):
            if (locations[8] == '' or locations[6] == ''):
                if (locations[7] == ''):
                    return True
        else:
            return False
    elif (request_info[1] == 'P'):
        if (locations[int(request_info[0])] == request_info[2]):
            return True
        else:
            return False


def update(bin_id, action):
    print(bin_id)
    temp_str = ''
    location_list = location_str.split('|')
    if (action == 0 or action == 5):
        location_list[action] = bin_id
    elif (action == 7):
        print("updating at location 7")
        if (location_list[7] == ''):
            location_list[action] = bin_id
        else:
            location_list[action] = ''

    for y in range(8):
        temp_str = temp_str + location_list[y]+'|'
    temp_str = temp_str + location_list[8]
    return temp_str


def move(start, end, direction):
    rotation_amnt = 0
    start_int = int(start)
    end_int = int(end)
    location_list = location_str.split('|')
    temporary_str = location_str
    temp_str = ''
    loop_count = 0
    print("start int is", start_int)
    if (start_int <= 5):
        while True:
            index_changed = False
            for move in moveOrders:
                starting_index = findStartIndex(move[4], temporary_str)
                available_index = findMoveableIndex(starting_index, move[3], temporary_str)
                if (available_index != starting_index):
                    print("moving the bin now from " + str(starting_index) + " to " + str(available_index))
                    location_list[available_index] = location_list[starting_index]
                    location_list[starting_index] = ''
                    temporary_str = ''
                    for y in range(5):
                        temporary_str = temporary_str + location_list[y]+'|'
                    temporary_str = temporary_str + location_list[5]
                    index_changed = True
                if (available_index == move[3]):
                    moveOrders.remove(move)
                    reply_to_return = "ST,"+str(sys.argv[1])+",J,"+move[0]+","+str(move[2])+"|"+str(move[3])+"|"+move[1]+"|"+move[4]+";"
                    s.send(reply_to_return.encode())
                    print(greenBright("Finished Moving"))
            if (index_changed is False):
                break
            else:
                loop_count = loop_count + 1
    elif (start_int == 7):
        if (location_list[end_int] == ''):
            location_list[end_int] = location_list[start_int]
            location_list[start_int] = ''
        else:
            if (end_int == 6):
                location_list[8] = location_list[start_int]
                location_list[start_int] = ''
    elif (start_int == 6):
        if (end_int == 7):
            if (location_list[7] == ''):
                location_list[7] = location_list[6]
                location_list[6] = ''
        if (end_int == 8):
            if(location_list[7] == '' and location_list[8] == ''):
                location_list[8] = location_list[6]
                location_list[6] = ''
    elif (start_int == 8):
        if (end_int == 7):
            if (location_list[7] == ''):
                location_list[7] = location_list[8]
                location_list[8] = ''
        if (end_int == 6):
            if(location_list[7] == '' and location_list[6] == ''):
                location_list[6] = location_list[8]
                location_list[8] = ''
    for y in range(8):
        temp_str = temp_str + location_list[y]+'|'
    temp_str = temp_str + location_list[8]
    return temp_str
    # return temperary_str


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
    s.send(("ST,"+str(sys.argv[1])+",P,Pairing;").encode())
    print(sys.argv[1])
    while True:
        data = s.recv(1024)
        decoded_data = data.decode()
        split_data = decoded_data.split(',')
        print("Received: "+decoded_data)
        if (split_data[0] == "ACK"):
            print("The server has acknowledged message.")
        elif ("ROTATION" in decoded_data):
            # Breakdown, move position and remake string
            location_reply = reply_breakdown(location_str)
            location_str = location_reply  # Update location_str with new value
            reply_to_return = "PLC1,ROTATION,JD,"+location_reply+",1;"
            s.send(reply_to_return.encode())
            print("Replied with: " + reply_to_return)
        elif ("ST,"+str(sys.argv[1])+",S;" in decoded_data):
            reply_to_return = "ST,"+str(sys.argv[1])+",S,"+location_str+";"
            s.send(reply_to_return.encode())
            print("Replied with: " + reply_to_return)
        elif ("ST,"+str(sys.argv[1])+",U" in decoded_data):
            reply_to_return = "ACK,"+decoded_data
            s.send(reply_to_return.encode())
            print(cyanBright("Replied with: " + reply_to_return))
            decoded_data = decoded_data.replace(';', '')
            split_data = decoded_data.split(",")
            bin_info = split_data[4].split("|")
            if(bin_info[0] == "0"):
                update_str = update(bin_info[2], 0)
            elif (bin_info[0] == "5"):
                update_str = update('', 5)
                location_str = update_str
                update_str = move(4, 5, 'A')
            elif (bin_info[0] == "7"):
                update_str = update(bin_info[2], 7)
                location_str = update_str
                locations = location_str.split('|')
                if (locations[7] == ''):
                    update_str = move('8', '6', 'A')
            location_str = update_str
            reply_to_return = "ST,"+str(sys.argv[1])+",S,"+location_str+";"
            s.send(reply_to_return.encode())
            print(cyanBright("Replied with: " + reply_to_return))
        elif ("ST,"+str(sys.argv[1])+",M" in decoded_data):
            reply_to_return = "ACK,"+decoded_data
            s.send(reply_to_return.encode())
            print(cyanBright("Replied with: " + reply_to_return))
            decoded_data = decoded_data.replace(';', '')
            split_data = decoded_data.split(",")
            move_info = split_data[4].split("|")
            start_index = move_info[0]
            end_index = move_info[1]
            direction = move_info[2]

            if(int(start_index) <= 5 and int(end_index) <= 5):
                moveOrders.append([split_data[3], direction, int(start_index), int(end_index), move_info[3]])
            new_locations = move(int(start_index), int(end_index), direction)
            location_str = new_locations
            if(int(start_index) <= 5 and int(end_index) <= 5):
                reply_to_return = "ST,"+str(sys.argv[1])+",S,"+location_str+";"
                s.send(reply_to_return.encode())
                print(cyanBright("Replied with: " + reply_to_return))
            else:
                reply_to_return = split_data[0]+","+split_data[1] + \
                    ",J,"+split_data[3]+","+split_data[4]+";"
                s.send(reply_to_return.encode())
                print(cyanBright("Replied with: "+reply_to_return))
                time.sleep(0.1)
                reply_to_return = "ST,"+str(sys.argv[1])+",S,"+location_str+";"
                s.send(reply_to_return.encode())
                print(cyanBright("Replied with: " + reply_to_return))

        elif ("ST,"+str(sys.argv[1])+",R" in decoded_data):
            decoded_data = decoded_data.replace(';', '')
            split_data = decoded_data.split(',')
            check_request = request(split_data[4])
            if check_request is True:
                reply_to_return = "ST,"+str(sys.argv[1])+",A,1,"+split_data[4]+";"
                s.send(reply_to_return.encode())
            else:
                reply_to_return = "ST,"+str(sys.argv[1])+",D,1,"+split_data[4]+";"
                s.send(reply_to_return.encode())
            print("Replied with: "+reply_to_return)
        elif ("ST,"+str(sys.argv[1])+",W" in decoded_data):
            decoded_data = decoded_data.replace(';', ',')
            print("decoded", decoded_data)
            reply_break_list = decoded_data.split(',')
            bin_id = reply_break_list[3]
            action = reply_break_list[4]
            print("bin_id is ", bin_id)
            check = database.findfakeBinExists(bin_id)

            print("check is", check)
            if check == 1:
                weight = 53
            else:
                random_no = random.randint(5, 6)
                if(action == "IN"):
                    weight = database.findfakeBinWeight(bin_id)+random_no
                if(action == "OUT"):
                    weight = database.findfakeBinWeight(bin_id)-random_no

            database.CreateUpdatefakeBinWeight(bin_id, weight, check)
            reply_to_return = decoded_data+str(weight)+";"
            s.send(reply_to_return.encode())
            print("Replied with: "+reply_to_return)
            print("weight", weight)
