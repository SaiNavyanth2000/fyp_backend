from flask import Flask, request,jsonify
from flask_cors import CORS
from matplotlib import pyplot as plt
from pandas_datareader import data as pdr
from datetime import date, timedelta
import yfinance as yf
from keras.models import load_model
import pandas as pd
import numpy as np
import pandas_ta as ta
from sklearn.preprocessing import MinMaxScaler
from model_ann import ann_model
from model_lstm import lstm_model
from model_multi_lstm import multi_lstm_model
import ast
# from flask import current_app
# current_app.config['SERVER_NAME'] = 'localhost'   
# with current_app.test_request_context():
#      url = url_for('index', _external=True)

today = date.today()
app = Flask(__name__)
Cors = CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}},CORS_SUPPORTS_CREDENTIALS = True)
app.config['CORS_HEADERS'] = 'Content-Type'

# cred_obj = firebase_admin.credentials.Certificate('../../fyp2022-stockpriceprediction-firebase-adminsdk-ku62m-f9ed330292.json')
# fyp_app = firebase_admin.initialize_app(cred_obj, {
# 	'databaseURL':"https://fyp2022-stockpriceprediction-default-rtdb.asia-southeast1.firebasedatabase.app/",
# 	'storageBucket': 'fyp2022-stockpriceprediction.appspot.com'
# 	})

@app.route("/predict", methods=["POST","GET"])
def submitData():
    print('habbfhkd')
    response_object = {'status':'success'}
    if request.method == "POST":
        #get arguments from request url https://stackabuse.com/get-request-query-parameters-with-flask/
        form_data = request.data
        data =  form_data.decode("UTF-8")
        data_dict = ast.literal_eval(data)
        print(data_dict)
        tick   = data_dict['ticker']
        model_type = data_dict['model_type']
        # response_object['prediction_value'] = 150

        def getTestData(ticker, start):
            data = pdr.get_data_yahoo(ticker, start=start, end=today)
            # dataname= ticker+"_"+str(today)
            return data[-101:-1]
                
        #find the starting date (100 trading days before today)
        #https://stackoverflow.com/questions/441147/how-to-subtract-a-day-from-a-date
        
        start = today - timedelta(days=290)
        df = getTestData(tick,start) 

        storing_data = df['Close'].copy().to_json() 
        response_object['past_100_days'] = storing_data

        # return response_object

        #custom ann
        if(model_type == 'ANN'):

            return ann_model(tick)
        
        #multivariate lstm
        elif model_type == 'MultiLstm':

            return multi_lstm_model(tick)
        
        #lstm for now
        else:
 
            return lstm_model(tick)       

if __name__ == '__main__':
    app.run(debug=True)