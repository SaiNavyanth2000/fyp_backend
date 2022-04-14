import pickle
from flask import jsonify
import os
from pandas_datareader import data as pdr
from datetime import date, timedelta
import yfinance as yf
from keras.models import load_model
import pandas as pd
import numpy as np
import json

def lstm_model(tick):
    response_object = {'status':'success'}
    today = date.today()
    scaler_path = "./data/normalizers/" + tick + "/lstm.pkl"
    model_path = "./data/models/" + tick + "/lstm"
    if(os.path.exists(model_path)):
        model = load_model(model_path)
    if(os.path.exists(scaler_path)):
        with open(scaler_path, "rb") as input_file:
            scaler = pickle.load(input_file)

    def getTestData(ticker, start):
        data = pdr.get_data_yahoo(ticker, start=start, end=today)
        # dataname= ticker+"_"+str(today)
        return data[-101:-1]
            
    #find the starting date (100 trading days before today)
    #https://stackoverflow.com/questions/441147/how-to-subtract-a-day-from-a-date
    
    start = today - timedelta(days=290)
    df = getTestData(tick,start) 

    storing_data = df['Close'].copy().to_json() 

    df = df.reset_index()['Close']

    df= scaler.transform(np.array(df).reshape(-1,1))
    test_data = df.reshape(-1,1)
            
    #https://datascience.stackexchange.com/questions/13461/how-can-i-get-prediction-for-only-one-instance-in-keras to get only one instance prediction
    test_data = np.array( [test_data,] ) 
            
    prediction = model.predict( test_data )
    prediction_value = scaler.inverse_transform(prediction)
            
    response_object['prediction_value'] = str(prediction_value[0][0])
    response_object['past_100_days'] = storing_data
    response_object['tick'] = tick     
    response_object['message'] ='Got data!'
    return jsonify(response_object)