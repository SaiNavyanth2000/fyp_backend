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
from sklearn.preprocessing import MinMaxScaler


def multi_lstm_model(tick):
    response_object = {'status':'success'}
    today = date.today()
    print('multi lstm model loading')
    scaler_x_path = "./data/normalizers/" + tick + "/multi_lstm_x.pkl"
    scaler_y_path = "./data/normalizers/" + tick + "/multi_lstm_y.pkl"
    model_path = "./data/models/" + tick + "/multi_lstm"
    pca_path = "./data/normalizers/" + tick + "/multi_lstm_pca.pkl"
    if(os.path.exists(model_path)):
        model = load_model(model_path)
    if(os.path.exists(scaler_x_path)):
        with open(scaler_x_path, "rb") as input_file:
            scaler_x = pickle.load(input_file)
    if(os.path.exists(scaler_y_path)):
        with open(scaler_y_path, "rb") as input_file:
            scaler_y = pickle.load(input_file)
    if(os.path.exists(pca_path)):
        with open(pca_path, "rb") as input_file:
            pca = pickle.load(input_file)
    

    def getTestData(ticker, start): 
        data = pdr.get_data_yahoo(ticker, start=start, end=today)
        # dataname= ticker+"_"+str(today)
        return data[-350:-1]
                
        
    start = today - timedelta(days=500)

    df = getTestData(tick,start) 
    storing_data = df['Close'].copy().to_json() 

    df['H-L'] = df['High'] - df['Low']
    df['O-C'] = df['Open'] - df['Close']
    df['5MA'] = df['Adj Close'].rolling(window=5).mean()
    df['10MA'] = df['Adj Close'].rolling(window=10).mean()
    df['20MA'] = df['Adj Close'].rolling(window=20).mean()
    df['7SD'] = df['Adj Close'].rolling(window=7).std()
    df["EMA8"] = df['Adj Close'].ewm(span=8).mean()
    df["EMA21"] = df['Adj Close'].ewm(span=21).mean()
    df['EMA34'] = df['Adj Close'].ewm(span=34).mean()
    df['EMA55'] = df['Adj Close'].ewm(span=55).mean()
    df.dropna(inplace=True)
    df['Returns'] = df['Close'] / df['Close'].shift(1)
    df['Returns'] -= 1
    df.dropna(inplace=True)
    df.ta.rsi(close='Close', length=14, append=True)
    df.dropna(inplace=True)

    features = ['Adj Close','H-L','O-C','5MA','10MA','20MA','7SD','RSI_14', 'EMA8','EMA21','EMA34','EMA55','Returns','Volume']
    df = df[features].apply(pd.to_numeric)
    df = df[-7:]
    features_x = ['H-L','O-C','5MA','10MA','20MA','7SD','RSI_14', 'EMA8','EMA21','EMA34','EMA55','Returns','Volume']
    scaled_x_data = scaler_x.transform(df[features_x])

    pca_data = pca.transform(scaled_x_data)
    # print(scaled_data.shape)
    scaled_data = pca_data.reshape((1,7,4))
    # sc_output = MinMaxScaler()

    # #https://stackoverflow.com/questions/49330195/how-to-use-inverse-transform-in-minmaxscaler-for-a-column-in-a-matrix
    # sc_output.min_ , sc_output.scale_ = scaler.min_[0], scaler.scale_[0]
    test_data = np.asarray(scaled_data, np.float32)
    pred = model.predict(test_data)  
    prediction_value = scaler_y.inverse_transform(pred)

    response_object['prediction_value'] = str(prediction_value[0][0])
    response_object['past_100_days'] = storing_data
    response_object['past_50_days'] = df.T.to_json()
    response_object['tick'] = tick
    response_object['message'] ='Got data!'
    return jsonify(response_object)