import numpy as np
import math, sys
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression

def predict_bikes_usage(arrayOfUsagePerDay, predictDays=1, previous_days_to_consider = 1):
    X = []
    y = []
    for i in range(len(arrayOfUsagePerDay)-previous_days_to_consider):
        train_part = arrayOfUsagePerDay[i:i+previous_days_to_consider]
        test_part = arrayOfUsagePerDay[i+previous_days_to_consider]        
        X.append(train_part)
        y.append(test_part)
    results = []
    for i in range(predictDays):

        reg = LinearRegression().fit(X, y)

        to_predict = arrayOfUsagePerDay[len(arrayOfUsagePerDay)-previous_days_to_consider:len(arrayOfUsagePerDay)]
        y_pred = reg.predict([to_predict])

        arrayOfUsagePerDay.append(y_pred[0]) #adding prediction to the list of values (needed to create the to_predict)
        X.append(to_predict) #adding train data point (needed for training)
        y.append(y_pred) #adding test data point (needed for training)
        results.append(y_pred) #adding prediction to results
    
    return math.ceil(results[0])