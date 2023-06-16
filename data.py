
import math
from flask import jsonify
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import uuid


def train(period,duration):
    
    data = pd.read_csv('files/sales.csv')
    print(data.info())
    x = [i for i in range(1,37)]
    y = data['Sales of shampoo over a three year period'].values
    x = np.reshape(x,(-1,1))
    y = np.reshape(y,(-1,1))

    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.33)

    poly = PolynomialFeatures(degree = 2)

    x_poly = poly.fit_transform(x_train)
    final = poly.transform(x_test)

    model = LinearRegression()
    model.fit(x_poly,y_train)
    result = model.predict(final)

    plt.plot(x,y)
    plt.title("Actual vs Predicted")
    plt.xlabel("Peroid in months")
    plt.ylabel("Sales of shampoo")
    plt.legend(loc='upper left')
    plt.scatter(x_test,result,color='red')

    r2score = r2_score(y_test,result)
    rmse = math.sqrt(np.square(np.subtract(y_test,result)).mean())

    if(period == 'Year'):
        duration *= 12
    duration+=36
    forecast = [i for i in range(36,duration+1)]
    forecast = np.reshape(forecast,(-1,1))
    dur = poly.transform(forecast)
    p = model.predict(dur)
    plt.plot(forecast,p,color='yellow')
    plt.legend(["Actual","Predicted","Forecast"])

    outid = uuid.uuid4()
    plt.savefig(f'files/{outid}.png')
    return jsonify({'id':str(outid),'r2':round(r2score,2),'rmse':round(rmse,2)})