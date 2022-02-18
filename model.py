import tensorflow as tf


class Model:
    def __init__(self):
        self.model = None
        self.input_data = None

    def set_model(self, model):
        self.model = tf.keras.models.load_model(model)

    def get_model(self):
        return self.model

    def set_input_data(self, input_data):
        self.input_data = input_data

    def get_input_data(self):
        return self.input_data

    def make_prediction(self):
        if self.get_model() is None:
            raise ValueError('No model provided')
        if self.get_input_data() is None:
            raise ValueError('No input data provided')

        # TODO: add prediciton logic

        return 0
