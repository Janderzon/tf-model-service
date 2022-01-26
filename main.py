import socket

PORT = 65432


def listen(PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', PORT))
        s.listen()
        return s.accept()


def readData(connection):
    data = []
    while True:
        newData = connection.recv(4096)
        if not newData:
            break
        data += newData
    return data
