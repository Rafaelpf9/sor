from socket import *

CLIENT_OPTIONS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
BUFFER_SIZE = 64000
INFO_MESSAGE = "SERVER_INFO"
SEPARATOR = "%"

def client_main():
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((gethostname(), 9000))
    response = get_answer(client, INFO_MESSAGE)
    final_response = parse_message(response)

    print("=" * 42)
    print("SERVER INFO")
    print("=" * 42)
    print(final_response)

    client.close()


def get_answer(client_socket, message):
    client_socket.send(message.encode('utf8'))
    response = client_socket.recv(BUFFER_SIZE).decode('utf8')
    return response

def parse_message(message_to_parse):
    parsed_message = message_to_parse.replace(SEPARATOR, '\n')
    return parsed_message


client_main()
