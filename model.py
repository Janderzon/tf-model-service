class Model:
    def __init__(self):
        self.model = None
        self.input_data = None

    def set_model(self, model):
        self.model = model

    def get_model(self):
        return self.model

    def set_input_data(self, input_data):
        self.input_data = input_data

    def get_input_data(self):
        return self.input_data
