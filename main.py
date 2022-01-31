import json
import socket
import tensorflow as tf
from tensorflow import keras
from requests import RequestProcessor

PORT = 65432


class InputDataManager:
    def __init__(self):
        self.data = None

    def set_input_data(self, data):
        self.data = data

    def get_input_data(self):
        return self.data


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


input_data_manager = InputDataManager()
request_processor = RequestProcessor()
connection, address = listen(PORT)
with connection:
    data = read_data(connection)
    json_data = json.loads(data)
    return_objs = []
    for json_obj in json_data:
        return_obj = request_processor.process_request(
            json_obj, input_data_manager)
        return_objs.append(return_obj)
    print(json.dumps(return_objs))
