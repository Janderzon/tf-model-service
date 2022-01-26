import socket

PORT = 65432


def listen(PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', PORT))
        s.listen()
        return s.accept()
