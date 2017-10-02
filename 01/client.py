from socket import *

CLIENT_OPTIONS = ["user_login", "os", "cpu_count", "server_directory"]
BUFFER_SIZE = 64000


def menu():
    info = """
    Options:
        User Login
        OS
        CPU Count
        Server directory
    """
    print(info)


def client_main():
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((gethostname(), 9000))

    while True:
        menu()
        option = input("Option: ").lower()

        # normalize user input
        user_option = option.replace(" ", "_")

        if user_option in CLIENT_OPTIONS:
            response = get_answer(client, user_option)
            print(response)
        else:
            print("Leave? ")
            answer = input('y/n: ').lower()
            if answer == 'y':
                client.send('kill'.encode('utf8'))
                break
            else:
                continue


def get_answer(client_socket, message):
    client_socket.send(message.encode('utf8'))
    response = client_socket.recv(BUFFER_SIZE).decode('utf8')
    return response

client_main()
