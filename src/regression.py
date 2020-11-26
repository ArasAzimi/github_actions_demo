from sklearn import linear_model

""" Regression class is to create a regression model """


class Regression:
    def __init__(self):
        self._model = None

    def createModel(self):
        self._model = linear_model.LinearRegression()
        return self._model
