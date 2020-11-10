import twitter_data
import stock_data
from twitter_data import data_creator_predict
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
import tensorflow as tf
from tf.python.keras.models import load_model
import json

def xScaler():
    x = np.array([[1.16666667, 0.66666667],[0.6131379 , 1.52368464],[0.9011529 , 1.42572293],[0.91221833, 1.75215763],[0.35060131, 1.75027643],[1.33333333, 0.93333333],[0.0, 2.79100529],[0.3488813 , 1.69110366],[1.0224359 , 3.37703963]])
    
    X_scaler = StandardScaler().fit(x)
    return X_scaler

def ml_data_formatter(data5): 
    try:
        data5['Price Change_up'].astype('int64')
    except:
        try:
            data5['Price Change_down'].astype('int64')
            if data5.iloc[0,3] == 1:
                data5.iloc[0,3] = 0
            else:
                data4.iloc[0,3] = 1
        except:
            try:
                data5 = data5.T
                data5['Price Change_up'].astype('int64')
            except:
                try:
                    data5['Price Change_down'].astype('int64')
                    if data5.iloc[0,3] == 1:
                        data5.iloc[0,3] = 0
                    else:
                        data4.iloc[0,3] = 1
                finally:
                    print('Not a valid company')
    data6x = []
    tempx = np.array([])
    for i in range(len(data5)):
        negative = data5.iloc[i,0]
        positive = data5.iloc[i,1]
        if i == 0:
            tempx = np.append(tempx, [negative, positive])
        else:
            tempx[0][0] += negative
            tempx[0][1] += positive
    data6x.append(tempx)
        
    #print(data6x)
    X = np.asarray(data6x)
    #print(X)
    X_scaler = xScaler()
    X_scaled = X_scaler.transform(X)
    
    return X_scaled

def get_sentiment(df):
    negative = []
    positive = []
    for i in range(len(df)):
        negative.append(df.iloc[i,0])
        positive.append(df.iloc[i,1])
    neg_avg = sum(negative)/len(negative)
    pos_avg = sum(positive)/len(positive)
    averages = [neg_avg, pos_avg]
    return averages

def stock_prediction(X, model):
    prediction = model.predict_classes(X)
    if prediction == 1:
        return 'Buy'
    else:
        return 'Sell'

def get_Prediction(company_name):
    model = load_model("Twitter_Sentiment_Stock_Model.h5")
    try:
        data = data_creator_predict(company_name)
    except:
        print('Not a valid company name')
        return None
    ml_data = ml_data_formatter(data)
    prediction = stock_prediction(ml_data, model)
    json_return = {}
    json_return["prediction"] = prediction
    averages = get_sentiment(data)
    json_return["positive"] = averages[1]
    json_return["negative"] = averages[0]
    json_return["Company_Name"] = company_name
    try:
        json_return["Closing_Prices"] = stock_data.find_ticker_data(company_name).iloc[-5:,0].tolist()
    except:
        print('Not a valid company name')
        return None
    json_return2 = json.dumps(json_return)
    return json_return2

if __name__ == '__main__':
    pass