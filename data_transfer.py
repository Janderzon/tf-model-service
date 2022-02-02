import socket


def read_data(connection):
    metadata = bytes()

    while True:
        metadata += connection.recv(4096)
        if len(metadata) >= 4:
            break

    data = metadata[4:]
    metadata = metadata[:4]
    data_len = int.from_bytes(metadata, 'little')

    while len(data) < data_len:
        data += connection.recv(4096)

    return data


def write_data(connection, msg):
    msg_len = len(msg)
    total_msg = msg_len.to_bytes(4, 'little') + msg
    connection.sendall(total_msg)
