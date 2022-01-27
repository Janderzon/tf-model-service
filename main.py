import socket
import json

PORT = 65432


def listen(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', port))
        s.listen()
        return s.accept()


def read_data(connection):
    data = bytes()
    while True:
        newData = connection.recv(4096)
        if not newData:
            break
        data += newData
    return data


connection, address = listen(PORT)
with connection:
    data = read_data(connection)
    data = json.loads(data)
    print(data['type'])
