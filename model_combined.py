import pickle
from flask import Flask, request,jsonify
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from pandas_datareader import data as pdr
from datetime import date, timedelta
import yfinance as yf
from keras.models import load_model
import pandas as pd
import numpy as np
import json
import pandas_ta as ta
from sklearn.preprocessing import MinMaxScaler

def combined_model_get_signal(tick):
    response_object = {}
    today = date.today()
    scaler_x_path = "./data/normalizers/" + tick + "/combination_model1_X.pkl"
    scaler_y_path = "./data/normalizers/" + tick + "/combination_model1_Y.pkl"
    model_path = "./data/models/" + tick + "/combination_model1"
    pca_path = "./data/normalizers/" + tick + "/combination_model1_pca.pkl"

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

    # import glob
    # print(glob.glob("./*"))

    def getTestData(ticker, start): 
        data = pdr.get_data_yahoo(ticker, start=start, end=today)
        # dataname= ticker+"_"+str(today)
        return data[-100:-1]
                    
            
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
    previous_closing_price = list(df['Close'])[-1]

    features = ['Adj Close','H-L','O-C','5MA','10MA','20MA','7SD','RSI_14', 'EMA8','EMA21','EMA34','EMA55','Returns','Volume']
    df = df[features].apply(pd.to_numeric)

    df = df[-7:]

    # date_today = '2022-04-13'
    print('got data till 7 days')
    # tick = 'GOOG'
    df_sentiment = pd.read_csv(f'./data/sentiment data/{today}_{tick}.csv')
    df['Vander_Score']= list(df_sentiment['Score'])
   
    features_x = ['H-L','O-C','5MA','10MA','20MA','7SD','RSI_14', 'EMA8','EMA21','EMA34','EMA55','Returns','Volume', 'Vander_Score']
    scaled_x_data = scaler_x.transform(df[features_x])

    x_test_pca = pca.transform(scaled_x_data)

    scaled_data = x_test_pca.reshape((1,7,4))

    test_data = np.asarray(scaled_data, np.float32)
    pred = model.predict(test_data)  
    prediction_value = scaler_y.inverse_transform(pred)
    # signal = ''
    print(prediction_value)
    if(prediction_value[0][0] > previous_closing_price):
        signal = 'Buy'
    else:
        signal = 'Sell'

    print(signal)

    response_object['prediction_value'] = signal
    response_object['past_100_days'] = storing_data
    response_object['past_50_days'] = df.T.to_json()
    response_object['tick'] = tick
    response_object['message'] ='Got data!'
    return jsonify(response_object)

