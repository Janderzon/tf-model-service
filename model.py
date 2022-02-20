import tensorflow as tf
import pandas as pd
import numpy as np
import datetime


class Model:
    def __init__(self):
        self.model = None
        self.input_data = None

    def _prep_data(self, data):
        data = data.dropna(how='all', axis='columns')

        date_time = pd.to_datetime(
            data.pop('Time'), format='%d/%m/%Y %H:%M')

        timestamp_s = date_time.map(datetime.datetime.timestamp)
        day = 24 * 60 * 60
        year = 365.2425 * day

        data['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
        data['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))
        data['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
        data['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))

        mean = data.mean()
        std = data.std()
        data = (data - mean) / std

        data = tf.convert_to_tensor(data)
        data = tf.reshape(data, [1, 24, 5])

        return data

    def set_model(self, model):
        self.model = tf.keras.models.load_model(model)

    def get_model(self):
        return self.model

    def set_input_data(self, input_data):
        input_data = pd.read_csv(input_data)
        self.input_data = self._prep_data(input_data)

    def get_input_data(self):
        return self.input_data

    def make_prediction(self):
        if self.get_model() is None:
            raise ValueError('No model provided')
        if self.get_input_data() is None:
            raise ValueError('No input data provided')

        # TODO: add prediciton logic

        return 0
