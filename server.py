import json
from threading import Thread
from socket import socket, gethostname, AF_INET, SOCK_DGRAM
from message_type import MessageType
from random import randint

# maps chat_name to -> [users_data] -> (user_names -> user_address), [rotations]
chat_metadata = {}

def rotate_n(word, n):
    result = ""
    for char in word:
        result += chr(ord(char) + n)
    return result

def encrypt_message(message, shift):
    return rotate_n(message, shift)

def decrypt_message(encrypted_message, shift_used_to_encrypt):
    return rotate_n(encrypted_message, shift_used_to_encrypt * -1)

BUFFER_SIZE = 64 * 1024 # 64kb

HOST = gethostname()
PORT = 9005
SERVER_ADDRESS = (HOST, PORT)

main_server_socket = socket(AF_INET, SOCK_DGRAM)

main_server_socket.bind(SERVER_ADDRESS)

def send_message_to_peers(client_address, message, encoded_message):

    group_name = message["group_name"]

    thread_socket = socket(AF_INET, SOCK_DGRAM)

    if group_name in chat_metadata:
        for user_name in chat_metadata[group_name]["users_data"]:
            if user_name == message["user_name"]:
                continue
            thread_socket.sendto(encoded_message, client_address)


def join_chat_group(client_address, message):
    response = {}

    group_name = message["group_name"]

    if group_name in chat_metadata:
        chat_metadata[group_name]["users_data"][message["user_name"]] = client_address
        response["status"] = "OK: Joined Group!"
    else:
        response["status"] = "ERROR: Group doesn't exists!"

    response_json = json.dumps(response)
    response_encoded = response_json.encode("utf8")

    socket(AF_INET, SOCK_DGRAM).sendto(response_encoded, client_address)


def create_chat_group(client_address, message):
    response = {}

    group_name = message["group_name"]

    if group_name in chat_metadata:
        response["status"] = "ERROR: Chat group already exists!"
    else:
        rotations = randint(5, 100)

        chat_metadata[group_name] = {}
        chat_metadata[group_name]["users_data"] = {message["user_name"], client_address}
        chat_metadata[group_name]["rotations"] = rotations

        response["status"] = "SUCCESS: Chat group and user registered!"
        response["rotations"] = rotations

    response_json = json.dumps(response)
    response_encoded = response_json.encode("utf8")

    socket(AF_INET, SOCK_DGRAM).sendto(response_encoded, client_address)


if __name__ == "__main__":
    print("Running...")

    while True:
        message_bytes, client_address = main_server_socket.recvfrom(BUFFER_SIZE)
        message_json = message_bytes.decode("utf8")
        message = json.loads(message_json)

        if message["type"] == MessageType.CREATE_GROUP:
            thread = Thread(target=create_chat_group, args=[client_address, message]).start()

        elif message["type"] == MessageType.JOIN_GROUP:
            thread = Thread(target=join_chat_group, args=[client_address, message])

        elif message["type"] == MessageType.NEW_MESSAGE:
            thread = Thread(target=send_message_to_peers, args=[client_address, message, message_bytes])