from socket import *
import os

addr = (gethostname(), 9000)
server = socket(AF_INET, SOCK_STREAM)
server.bind(addr)


def server_main():
    server.listen(100)

    client, client_address = server.accept()
    while True:
        client_option = client.recv(1024).decode('utf8')
        if client_option == 'os':
            response = os.name
            client.send(response.encode('utf8'))
        elif client_option == 'user_login':
            response = os.getlogin()
            client.send(response.encode('utf8'))
        elif client_option == 'cpu_count':
            response = str(os.cpu_count())
            client.send(response.encode('utf8'))
        elif client_option == 'server_directory':
            response = str(os.getcwd())
            client.send(response.encode('utf8'))
        else:
            client.close()
            break

while True:
    server_main()
