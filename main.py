import json
import socket
import tensorflow as tf
from tensorflow import keras

PORT = 65432


class ReturnObjectManager:
    def __init__(self, type):
        self.dict = dict()
        self.dict['type'] = type

    def set_succeeded(self, success):
        self.dict['succeeded'] = success

    def set_return_data(self, data):
        self.dict['data'] = data

    def set_error_message(self, message):
        self.dict['error'] = message

    def get_return_obj(self):
        return self.dict

    def contains(self, key):
        if key in self.dict:
            return True
        return False


class Model:
    def __init__(self):
        self.model = None

    def set_model(self, model):
        self.model = model

    def get_model(self):
        return self.model


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


def process_request(json_obj, model, data):
    request_type = json_obj['type']
    if request_type == 'model':
        return read_model(json_obj, model)

    elif request_type == 'input_data':
        return read_input_data(json_obj, data)

    elif request_type == 'predict':
        return make_prediction(model, data)


def read_model(json_obj, model):
    obj_manager = ReturnObjectManager('read_model')

    if obj_manager.contains('model'):
        model.set_model(json_obj['model'])
        obj_manager.set_succeeded(True)
    else:
        obj_manager.set_error_message('No model provided')
        obj_manager.set_succeeded(False)

    return obj_manager.get_return_obj()


def read_input_data(json_obj, data):
    obj_manager = ReturnObjectManager('loaded_input_data')

    if obj_manager.contains('data'):
        data.set_input_data(json_obj['data'])
        obj_manager.set_succeeded(True)
    else:
        obj_manager.set_error_message('No input data provided')
        obj_manager.set_succeeded(False)

    return obj_manager.get_return_obj()


def make_prediction(model, data):
    obj_manager = ReturnObjectManager('made_prediction')
    obj_manager.set_succeeded(False)

    model = model.get_model()
    data = data.get_input_data()

    if model is None:
        obj_manager.set_error_message('No model loaded')
        return obj_manager.get_return_obj()

    if data is None:
        obj_manager.set_error_message('No input data')
        return obj_manager.get_return_obj()

    return obj_manager.get_return_obj()


model = Model()
input_data_manager = InputDataManager()
connection, address = listen(PORT)
with connection:
    data = read_data(connection)
    json_data = json.loads(data)
    return_objs = []
    for json_obj in json_data:
        return_obj = process_request(json_obj, model, input_data_manager)
        return_objs.append(return_obj)
    print(json.dumps(return_objs))
