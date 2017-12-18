import json
from threading import Thread
from socket import socket, gethostname, AF_INET, SOCK_DGRAM
from message_type import MessageType
from random import randint

BUFFER_SIZE = 64 * 1024 # 64kb

HOST = gethostname()
PORT = 9005
SERVER_ADDRESS = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_DGRAM)

user_name = input("Your user name: ")

options = ["Create a new group", "Connect to a new group"]

print("Initial options..")

[print(option) for option in options]

user_option = input("Option: ")

if user_option == options[0]:
    group_name = input("Group name: ")
    message = {}
    message["group_name"] = group_name
    message["user_name"] = user_name
    message["type"] = MessageType.CREATE_GROUP
    client_socket.sendto(json.dumps(message).encode("utf8"), SERVER_ADDRESS)
    response, _ = client_socket.recvfrom(BUFFER_SIZE)
    print(response.decode("utf8"))
