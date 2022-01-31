import json
import socket
import sys
import tensorflow as tf
from tensorflow import keras

PORT = 65432
_model = None


class ReturnObject:
    def __init__(self, type):
        self.dict = dict()
        self.dict['type'] = type

    def get(self):
        return self.dict

    def set_succeeded(self, success):
        self.dict['succeeded'] = success

    def set_return_data(self, data):
        self.dict['data'] = data

    def set_error_message(self, message):
        self.dict['error'] = message

    def contains(self, key):
        if key in self.dict:
            return True
        return False


def set_model(model):
    _model = model


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


def process_request(json_obj):
    request_type = json_obj['type']
    if request_type == 'model':
        return read_model(json_obj)
    elif request_type == 'input_data':
        return read_input_data(json_obj)
    elif request_type == 'predict':
        return make_prediction()


def read_model(json_obj):
    return_obj = ReturnObject('read_model')

    if return_obj.contains('model'):
        set_model(json_obj['model'])
        return_obj.set_succeeded(True)
    else:
        return_obj.set_error_message('No model provided')
        return_obj.set_succeeded(False)

    return json.dumps(return_obj.get())


def read_input_data(json_obj):
    return_obj = ReturnObject('loaded_input_data')
    return_obj.set_succeeded(False)
    return json.dumps(return_obj.get())


def make_prediction():
    return_obj = ReturnObject('made_prediction')
    return_obj.set_succeeded(False)
    return json.dumps(return_obj.get())


connection, address = listen(PORT)
with connection:
    data = read_data(connection)
    json_data = json.loads(data)
    return_objs = []
    for json_obj in json_data:
        return_objs.append(process_request(json_obj))
    print(return_objs)
