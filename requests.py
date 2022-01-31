from model import Model


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


class RequestProcessor:
    def __init__(self):
        self.model = Model()

    def _read_model(self, json_obj):
        obj_manager = ReturnObjectManager('read_model')

        if obj_manager.contains('model'):
            self.model.set_model(json_obj['model'])
            obj_manager.set_succeeded(True)
        else:
            obj_manager.set_error_message('No model provided')
            obj_manager.set_succeeded(False)

        return obj_manager.get_return_obj()

    def _read_input_data(self, json_obj):
        obj_manager = ReturnObjectManager('loaded_input_data')

        if obj_manager.contains('data'):
            self.model.set_input_data(json_obj['data'])
            obj_manager.set_succeeded(True)
        else:
            obj_manager.set_error_message('No input data provided')
            obj_manager.set_succeeded(False)

        return obj_manager.get_return_obj()

    def _make_prediction(self):
        obj_manager = ReturnObjectManager('made_prediction')
        obj_manager.set_succeeded(False)

        model = self.model.get_model()
        data = self.model.get_input_data()

        if model is None:
            obj_manager.set_error_message('No model loaded')
            return obj_manager.get_return_obj()

        if data is None:
            obj_manager.set_error_message('No input data')
            return obj_manager.get_return_obj()

        return obj_manager.get_return_obj()

    def process_request(self, json_obj):
        request_type = json_obj['type']
        if request_type == 'model':
            return self._read_model(json_obj)

        elif request_type == 'input_data':
            return self._read_input_data(json_obj)

        elif request_type == 'predict':
            return self._make_prediction()
