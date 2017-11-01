from socket import socket, gethostname, AF_INET, SOCK_DGRAM
import json

class Client:

    COMMANDS = ["insert", "remove", "query", "query_all"]
    QUANTITY_OF_BYTES = 1024 * 64

    def __init__(self, server_address):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.server_address = server_address


    def insert(self, key, value):
        command_encoded = "insert".encode("utf8")
        data = dict()
        data[key] = value
        json_data_encoded = json.dumps(data).encode("utf8")

        self.socket.sendto(command_encoded, self.server_address)
        self.socket.sendto(json_data_encoded, self.server_address)

    def query(self, key):
        command_encoded = "query".encode("utf8")
        key_encoded = key.encode("utf8")

        self.socket.sendto(command_encoded, self.server_address)
        self.socket.sendto(key_encoded, self.server_address)

        response_data, server_address = self.socket.recvfrom(Client.QUANTITY_OF_BYTES)
        response = response_data.decode("utf8")

        return response

    def fun(self, value):
        print(value)

    def menu(self):
        print("=" * 75)
        print("Commands")
        print("=" * 75)

        for command in Client.COMMANDS:
            print(command)

        print("=" * 75)

    def run(self):
        self.menu()
        client_option = input("Your command: ").lower()

        if client_option in Client.COMMANDS:
            if client_option == "insert":
                key = input("Abbreviation: ")
                value = input("Meaning: ")

                self.insert(key, value)
            elif client_option == "query":
                key = input("Which key to search: ")

                result = self.query(key)
                print(result)
        else:
            print("Insert a valid command!")


if __name__ == "__main__":
    SERVER_ADDRESS = (gethostname(), 9000)

    client = Client(SERVER_ADDRESS)
    client.run()