import socket
import json

PORT = 65432


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
    return '{"read_model":"false"}'


def read_input_data(json_obj):
    return '{"loaded_input_data":"false"}'


def make_prediction():
    return '{"made_prediction":"false"}'


connection, address = listen(PORT)
with connection:
    data = read_data(connection)
    json_data = json.loads(data)
    return_objs = []
    for json_obj in json_data:
        return_objs.append(process_request(json_obj))
    print(return_objs)
