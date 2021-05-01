import numpy as np
import math
import sys
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
from ..Config.config_handler import read_config

config_vals = read_config("Footfall_API")

# Time Series Prediction algorithm to predict the avaerage footfall count for days ahead
def predict_footfall(arrayOfFootfallData, predictDays=1, previous_days_to_consider=config_vals["days_to_consider_for_prediction"]):
    X = []
    y = []
    for i in range(len(arrayOfFootfallData)-previous_days_to_consider):
        train_part = arrayOfFootfallData[i:i+previous_days_to_consider]
        test_part = arrayOfFootfallData[i+previous_days_to_consider]
        X.append(train_part)
        y.append(test_part)
    results = []
    for i in range(predictDays):

        reg = LinearRegression().fit(X, y)

        to_predict = arrayOfFootfallData[len(
            arrayOfFootfallData)-previous_days_to_consider:len(arrayOfFootfallData)]
        y_pred = reg.predict([to_predict])

        # adding prediction to the list of values (needed to create the to_predict)
        arrayOfFootfallData.append(y_pred[0])
        X.append(to_predict)  # adding train data point (needed for training)
        y.append(y_pred)  # adding test data point (needed for training)
        results.append(y_pred)  # adding prediction to results

    return math.ceil(results[0])
