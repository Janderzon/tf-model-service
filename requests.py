from model import Model


class _ReturnObjectManager:
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


class RequestProcessor:
    def __init__(self):
        self.model = Model()

    def _read_model(self, json_obj):
        obj_manager = _ReturnObjectManager('read_model')

        if 'model' in json_obj:
            self.model.set_model(json_obj['model'])
            obj_manager.set_succeeded(True)
        else:
            obj_manager.set_error_message('No model provided')
            obj_manager.set_succeeded(False)

        return obj_manager.get_return_obj()

    def _read_input_data(self, json_obj):
        obj_manager = _ReturnObjectManager('loaded_input_data')

        if 'data' in json_obj:
            self.model.set_input_data(json_obj['data'])
            obj_manager.set_succeeded(True)
        else:
            obj_manager.set_error_message('No input data provided')
            obj_manager.set_succeeded(False)

        return obj_manager.get_return_obj()

    def _make_prediction(self):
        obj_manager = _ReturnObjectManager('made_prediction')

        try:
            obj_manager.set_return_data(self.model.make_prediction())
            obj_manager.set_succeeded(True)
        except ValueError as e:
            obj_manager.set_error_message(str(e))
            obj_manager.set_succeeded(False)

        return obj_manager.get_return_obj()

    def process_request(self, json_obj):
        request_type = json_obj['type']
        if request_type == 'model':
            return self._read_model(json_obj)

        elif request_type == 'input_data':
            return self._read_input_data(json_obj)

        elif request_type == 'predict':
            return self._make_prediction()
