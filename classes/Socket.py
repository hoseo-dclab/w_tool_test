from classes import customException
from socket import *


class Socket:
    def __init__(self):
        self.client = socket(AF_INET, SOCK_STREAM)


def connect(address):
    client_socket = Socket()

    if address.count(':') == 1:
        HOST, PORT = address.split(':')
        ADDR = (HOST, int(PORT))
    else:
        ADDR = (address,)

    try:
        client = client_socket.client.connect(ADDR)
    except:
        raise customException.raise_exception("address가 일치하지 않습니다.")

    return client
