import json
import socket
import tensorflow as tf
import data_transfer
from tensorflow import keras
from requests import RequestProcessor

PORT = 65432


def listen(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', port))
        s.listen()

        return s.accept()


request_processor = RequestProcessor()
connection, address = listen(PORT)
with connection:
    data = data_transfer.read_data(connection)
    json_data = json.loads(data)

    return_objs = []
    for json_obj in json_data:
        return_obj = request_processor.process_request(json_obj)
        return_objs.append(return_obj)

    return_str = json.dumps(return_objs)
    return_bytes = return_str.encode('utf-8')

    data_transfer.write_data(connection, return_bytes)
