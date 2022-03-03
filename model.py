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
            data.pop('OpenTime'), format='%d/%m/%Y %H:%M:%S')

        timestamp_s = date_time.map(datetime.datetime.timestamp)
        day = 24 * 60 * 60
        week = 7 * day
        year = 365.2425 * day
        month = year / 12

        data['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
        data['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))
        data['Week sin'] = np.sin(timestamp_s * (2 * np.pi / week))
        data['Week cos'] = np.cos(timestamp_s * (2 * np.pi / week))
        data['Month sin'] = np.sin(timestamp_s * (2 * np.pi / month))
        data['Month cos'] = np.cos(timestamp_s * (2 * np.pi / month))
        data['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
        data['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))

        self.mean = data['OpenPrice'].mean()
        self.std = data['OpenPrice'].std()

        mean = data.mean()
        std = data.std()
        data = (data - mean) / std

        data = tf.convert_to_tensor(data)
        data = tf.reshape(data, [1, 5, 9])

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

        prediction = self.model.predict(self.input_data)
        return float(prediction) * self.std + self.mean
