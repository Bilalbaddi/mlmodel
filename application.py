from flask import Flask,render_template,request,redirect,url_for
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle

application = Flask(__name__)
app = application
lasso_model = pickle.load(open('model/lassocv.pkl','rb'))
scaler = pickle.load(open('model/scaler.pkl','rb'))


@app.route('/')
def index():
    return "Welcome to my Flask App! it is an amazing course"
@app.route('/predictdata'  ,methods = ['GET','POST'])

def predict_datapoint():
    if request.method == 'POST':
        try:
            # Extract form data
            temperature = float(request.form.get('temperature', 0))
            rh = float(request.form.get('rh', 0))
            ws = float(request.form.get('ws', 0))
            rain = float(request.form.get('rain', 0))
            ffmc = float(request.form.get('ffmc', 0))
            dmc = float(request.form.get('dmc', 0))
            isi = float(request.form.get('isi', 0))
            classes = float(request.form.get('classes', 0))
            region = float(request.form.get('region', 0))

            # Combine the inputs into a single 2D array
            new_data = np.array([[temperature, rh, ws, rain, ffmc, dmc, isi, classes, region]])

            # Scale the data
            scaled_data = scaler.transform(new_data)

            # Make a prediction
            result = lasso_model.predict(scaled_data)[0]

            # Render the template with the result
            return render_template('home.html', results=f"Predicted Value: {result:.2f}")
        except Exception as e:
            # Handle any errors and return an error message
            return render_template('home.html', results=f"Error: {str(e)}")
    else:
        # For GET requests, simply render the form
        return render_template('home.html')




if __name__ == "__main__":
    app.run('0.0.0.0',debug= True)
