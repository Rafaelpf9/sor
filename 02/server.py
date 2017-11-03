from socket import *
import platform

SEPARATOR = "%"
addr = (gethostname(), 9000)
server = socket(AF_INET, SOCK_STREAM)
server.bind(addr)


def server_main():
    client, client_address = server.accept()

    response = ""

    response += "Processor: {} {}".format(platform.processor(), SEPARATOR)

    response += "Processor architecture: {} {}".format(platform.machine(), SEPARATOR)

    response += "System architecture: {} {}".format(platform.architecture()[0], SEPARATOR)

    response += "Operating System: {} {}".format(platform.system(), SEPARATOR)

    response += "System version: {} {}".format(platform.version(), SEPARATOR)

    response += "System release: {} {}".format(platform.release(), SEPARATOR)

    response += "Network: {} {}".format(platform.node(), SEPARATOR)

    response += "Python version: {} {}".format(platform.python_version(), SEPARATOR)

    response += "Python implementation: {} {}".format(platform.python_implementation(), SEPARATOR)

    response += "Python compiler: {} {}".format(platform.python_compiler(), SEPARATOR)

    client.send(response.encode('utf8'))

    client.close()


server.listen(1000)
while True:
    server_main()
