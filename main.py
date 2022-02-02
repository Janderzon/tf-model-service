import json
import socket
import tensorflow as tf
from tensorflow import keras
from requests import RequestProcessor

PORT = 65432


def listen(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', port))
        s.listen()

        return s.accept()


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


request_processor = RequestProcessor()
connection, address = listen(PORT)
with connection:
    data = read_data(connection)
    json_data = json.loads(data)
    return_objs = []
    for json_obj in json_data:
        return_obj = request_processor.process_request(json_obj)
        return_objs.append(return_obj)
    return_str = json.dumps(return_objs)
    return_bytes = return_str.encode('utf-8')
    connection.sendall(return_bytes)
