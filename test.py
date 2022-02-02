import socket


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


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    msg = b'[{"type":"model"}, {"type":"input_data"}, {"type":"predict"}]'
    msg_len = len(msg)
    s.sendall(msg_len.to_bytes(4, 'little')+msg)
    return_msg = read_data(s)
    print(return_msg.decode('utf-8'))
