from socket import socket, gethostname, AF_INET, SOCK_DGRAM
import json

class Server:

    COMMANDS = ["insert", "remove", "query", "query_all"]
    QUANTITY_OF_BYTES = 1024 * 64

    def __init__(self, server_address):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(server_address)

        dictionary_data_file = open("result.txt", "r")
        self.dictionary = json.load(dictionary_data_file)

    def insert_command(self, key, value):
        self.dictionary[key] = value

    def query_command(self, key, client_address):
        response = ""

        if key in self.dictionary:
            response = self.dictionary[key]
        else:
            response = "Key not found!"

        self.socket.sendto(response.encode("utf8"), client_address)

    def get_all_command(self, client_address):
        json_data = json.loads(self.dictionary).encode("utf8")
        self.socket.sendto(json, client_address)

    def remove_command(self, key):
        self.dictionary.pop(key, None)

    def run(self):

        client_option_data, client_address = \
            self.socket.recvfrom(Server.QUANTITY_OF_BYTES)

        client_option = client_option_data.decode("utf8")
        print(client_option)
        if client_option in Server.COMMANDS:

            if client_option == "insert":
                json_data, client_address = \
                    self.socket.recvfrom(Server.QUANTITY_OF_BYTES)

                insertion_json = json_data.decode("utf8")
                insertion_dictionary = json.loads(insertion_json)
                key_value_tuple = insertion_dictionary.popitem()

                key = key_value_tuple[0]
                value = key_value_tuple[1]

                self.insert_command(key, value)

            elif client_option == "remove":
                remove_key_encoded, client_address = \
                    self.socket.recvfrom(Server.QUANTITY_OF_BYTES)

                remove_key = remove_key_encoded.decode("utf8")

                self.remove_command(remove_key)

            elif client_option == "query":
                query_key_encoded, client_address = \
                    self.socket.recvfrom(Server.QUANTITY_OF_BYTES)

                query_key = query_key_encoded.decode("utf8")

                self.query_command(query_key, client_address)



if __name__ == "__main__":
    server = Server((gethostname(), 9000))
    server.run()