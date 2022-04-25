from flask import Flask, request,jsonify
from flask_cors import CORS
from model_ann import ann_model
from model_lstm import lstm_model
from model_multi_lstm import multi_lstm_model
from model_combined import combined_model_get_signal
import ast
import gc

#initialize flask app
app = Flask(__name__)
Cors = CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}},CORS_SUPPORTS_CREDENTIALS = True)
app.config['CORS_HEADERS'] = 'Content-Type'



@app.route("/predict", methods=["POST","GET"])
def submitData():

    response_object = {'status':'success'}

    if request.method == 'GET':
        return 'got a invalid GET request'

    if request.method == "POST":
        #get arguments from request url https://stackabuse.com/get-request-query-parameters-with-flask/
        try:
            form_data = request.data
            data =  form_data.decode("UTF-8")
            data_dict = ast.literal_eval(data)
    
            tick   = data_dict['ticker']
            model_type = data_dict['model_type']
        except:
            tick = 'AAPL'
            model_type = 'lstm'

        #custom ann
        if(model_type == 'ANN'):

            response_object =  ann_model(tick)
        
        #multivariate lstm
        elif model_type == 'MultiLstm':

            response_object = multi_lstm_model(tick)
        
        #combined model
        elif model_type == 'Combined':

            response_object =  combined_model_get_signal(tick)

        #lstm
        else: 

            response_object = lstm_model(tick)   


        # garbage collection https://www.geeksforgeeks.org/memory-leak-in-python-requests/
        gc.collect()   

        return response_object    

if __name__ == '__main__':
    app.run(debug=True)