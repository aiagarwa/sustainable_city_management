import numpy as np
import math, sys
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression

# Original one
def predictBikesUsage(arrayOfUsagePerDay):
    arrayOfUsagePerDay = np.array(arrayOfUsagePerDay)

    dt = 24*60*60 # data sampling interval in seconds
    t = range(len(arrayOfUsagePerDay))
    y = arrayOfUsagePerDay
    # plot extracted data
    # plt.scatter(t,y, color='red', marker='.'); plt.show()

    # predictBikesUsage([4, 10, 2, 8, 4])

    ###############
    # Predictions #
    ###############

    # def test_preds(q,dd,lag,plot):
    #     #q-step ahead prediction
    #     stride=1
    #     XX=y[0:y.size-q-lag*dd:stride]
    #     for i in range(1,lag):  
    #         X=y[i*dd:y.size-q-(lag-i)*dd:stride]
    #         XX=np.column_stack((XX,X))

    #     yy=y[lag*dd+q::stride]; tt=t[lag*dd+q::stride]
    #     train, test = train_test_split(np.arange(0,yy.size),test_size=0.2)
    #     model = Ridge(fit_intercept=False).fit(XX[train], yy[train])
    #     print(model.intercept_, model.coef_)
    #     if plot:
    #         y_pred = model.predict(XX)
    #         plt.scatter(t, y, color='black'); plt.scatter(tt, y_pred, color='blue')
    #         plt.xlabel("time (days)"); plt.ylabel("#bikes")
    #         plt.legend(["training data","predictions"],loc='upper right')
    #         day=math.floor(24*60*60/dt) # number of samples per day
    #         plt.xlim(((lag*dd+q)/day,(lag*dd+q)/day+2))
    #         plt.show()

    # # prediction using short-term trend
    # plot=True
    # test_preds(q=10,dd=1,lag=3,plot=plot)

    # # prediction using daily seasonality
    # d=math.floor(24*60*60/dt) # number of samples per day
    # test_preds(q=d,dd=d,lag=3,plot=plot)

    # # prediction using weekly seasonality
    # w=math.floor(7*24*60*60/dt) # number of 


    #######################
    # Putting it together #
    #######################

    plot=True
    #putting it together
    q=1
    lag=1; stride=7
    w=math.floor(7*24*60*60/dt) # number of samples per week

    len = y.size-w-lag*w-q
    XX=y[q:q+len:stride]

    for i in range(1,lag):
        X=y[i*w+q:i*w+q+len:stride]
        XX=np.column_stack((XX,X))

    d=math.floor(24*60*60/dt) # number of samples per day

    for i in range(0,lag):
        X=y[i*d+q:i*d+q+len:stride]
        XX=np.column_stack((XX,X))

    for i in range(0,lag):
        X=y[i:i+len:stride]
        XX=np.column_stack((XX,X))

    yy=y[lag*w+w+q:lag*w+w+q+len:stride]
    tt=t[lag*w+w+q:lag*w+w+q+len:stride]
    train, test = train_test_split(np.arange(0,yy.size),test_size=0.2)
    model = Ridge(fit_intercept=False).fit(XX[train], yy[train])
    print(model.intercept_, model.coef_)

    if plot:
        y_pred = model.predict(XX)
        plt.scatter(t, y, color='black'); plt.scatter(tt, y_pred, color='blue', marker='+')
        plt.xlabel("time (days)"); plt.ylabel("#bikes")
        plt.legend(["training data","predictions"],loc='upper right')
        day=math.floor(24*60*60/dt) # number of samples per day
        plt.show()
    
    return y_pred # return predictions

def predictBikesUsageTest(arrayOfUsagePerDay):
    previous_days_to_consider = 3

    X = []
    y = []
    for i in range(len(arrayOfUsagePerDay)-previous_days_to_consider):
        train_part = arrayOfUsagePerDay[i:i+previous_days_to_consider]
        test_part = arrayOfUsagePerDay[i+previous_days_to_consider]
        
        X.append(train_part)
        y.append(test_part)

    reg = LinearRegression().fit(X, y)
    to_predict = arrayOfUsagePerDay[len(arrayOfUsagePerDay)-previous_days_to_consider:len(arrayOfUsagePerDay)]
    print(reg.predict([to_predict]))
    return reg.predict([to_predict])