import socket
import data_transfer


def listen(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', port))
        s.listen()

        return s.accept()


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data_transfer.write_data(
        s, b'[{"type":"model"}, {"type":"input_data"}, {"type":"predict"}]')
    return_msg = data_transfer.read_data(s)
    print(return_msg.decode('utf-8'))
