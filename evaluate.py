import numpy as np
from sklearn.linear_model import LinearRegression


class EvaluationModel(object):
    def __init__(self, model=LinearRegression):
        self._model = model()
        self._last_prediction = None

    def fit(self, x, y):
        self._model.fit(x, y)

    def predict(self, x):
        self._last_prediction = self._model.predict(x)
        return self.last_prediction

    @property
    def last_prediction(self):
        return self._last_prediction

    def evaluate_error_from_last_prediction(self, expected_results):
        if self.last_prediction is None:
            return None
        errors = []
        for (predictedValue, trueValue) in zip(self.last_prediction, expected_results):
            errors.append(int(trueValue - predictedValue))
        mean = np.mean(errors)
        average = np.average(errors)
        minimum = np.min(errors)
        maximum = np.max(errors)
        std = np.std(errors)
        std_percentage = std / np.max(expected_results) * 100
        return errors, mean, average, minimum, maximum, std, std_percentage
