from flask import Flask,render_template,request 
import jsonify 
import requests 
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app=Flask(_name_)
model = pickle.load(open('random_forest_regression_model.pkl','rb'))
@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route('/predict', methods=['POST'])
def predict():
    Fuel_Type_Disel = 0
    if request.methods == 'POST':
        Year=int(request.form['Year'])
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2 = np.log(Kms_Driven)
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol == 'Petrol'):
            Fuel_Type_Petrol = 1
            Fuel_Type_Disel = 0
        elif(Fuel_Type_Petrol=='Disel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Disel = 1
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Disel=0
        Year=2020-Year
        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0
        Transmission_Mannual = request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Manual=0
        prediction=model.predict([[Present_Price,Kms_Driven,Owner,Year,Fuel_Type_Petrol,Fuel_Type_Disel,Seller_Type_Individual,Transmission_Manual,]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you can not sell this car")
        else:
            return render_template('index.html',prediction_text="You can sell the car at {}".format(output))
    else:
        return render_template('index.html')
    
if _name_== "_main_":
    app.run(debug=True)
