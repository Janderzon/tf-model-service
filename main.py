import socket
from urllib import request

PORT = 65432


def listen(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', port))
        s.listen()
        return s.accept()


def read_data(connection):
    data = []
    while True:
        newData = connection.recv(4096)
        if not newData:
            break
        data += newData
    return data


def split_data(data):
    request_type = int.from_bytes(data[:4], 'little')
    raw_data = bytes(data[4:])
    return request_type, raw_data


connection, address = listen(PORT)
with connection:
    data = read_data(connection)
    request_type, raw_data = split_data(data)
    print(request_type)
    print(str(raw_data))
