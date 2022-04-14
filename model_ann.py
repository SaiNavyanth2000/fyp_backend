import pickle
from flask import Flask, request,jsonify
import os
from pandas_datareader import data as pdr
from datetime import date, timedelta
import yfinance as yf
from keras.models import load_model
import pandas as pd
import numpy as np
import json
import pandas_ta as ta


def ann_model(tick):
    print('ann model loading')
    response_object = {'status':'success'}
    today = date.today()
    scaler_path = "../../data/normalizers/" + tick + "/ann_x.pkl"
    model_path = "../../data/models/" + tick + "/ann"
    if(os.path.exists(model_path)):
        model = load_model(model_path)
    if(os.path.exists(scaler_path)):
        with open(scaler_path, "rb") as input_file:
            scaler_x = pickle.load(input_file)
    scaler_path = "../../data/normalizers/" + tick + "/ann_y.pkl"
    if(os.path.exists(scaler_path)):
        with open(scaler_path, "rb") as input_file:
            scaler_y = pickle.load(input_file)

    def getTestData(ticker, start):
        data = pdr.get_data_yahoo(ticker, start=start, end=today)
        # dataname= ticker+"_"+str(today)
        return data[-101:-1]
            
    #find the starting date (100 trading days before today)
    #https://stackoverflow.com/questions/441147/how-to-subtract-a-day-from-a-date
    
    start = today - timedelta(days=290)
    df = getTestData(tick,start) 

    storing_data = df['Close'].copy().to_json()   

    df['H-L'] = df['High'] - df['Low']
    df['O-C'] = df['Open'] - df['Close']
    df['7MA'] = df['Adj Close'].rolling(window=7).mean()
    df['14MA'] = df['Adj Close'].rolling(window=14).mean()
    df['21MA'] = df['Adj Close'].rolling(window=21).mean()
    df['7SD'] = df['Adj Close'].rolling(window=7).std()
    features = ['H-L','O-C','7MA','14MA','21MA','7SD','Volume']
    test_data = np.asarray(df[-1:][features], np.float32)
    test = scaler_x.transform(test_data)
            
    prediction = model.predict(test)  
    prediction_value = scaler_y.inverse_transform(prediction)

    response_object['prediction_value'] = str(prediction_value[0][0])
    response_object['past_100_days'] = storing_data
    response_object['tick'] = tick      
    response_object['message'] ='Got data!'

    return jsonify(response_object)