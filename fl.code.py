import numpy as np
import pickle
import pandas as pd
#from flasgger import Swagger
import streamlit as st 

from PIL import Image

#app=Flask(name)
#Swagger(app)

pickle_in = open("stacking_model_N.pkl","rb")
stacking_model_N=pickle.load(pickle_in)

pickle_in = open("stacking_model_P.pkl","rb")
stacking_model_P=pickle.load(pickle_in)

pickle_in = open("stacking_model_K.pkl","rb")
stacking_model_K=pickle.load(pickle_in)

#@app.route('/')
def welcome():
    return "Welcome All"

#@app.route('/predict',methods=["Get"])
def predict__amount_of_fertilizer(N, P, K, temperature, humidity, ph, rainfall, label):
    input=[[temperature, humidity, ph, rainfall, label]]
    # Calculate deficiencies using a function
    try:
        predicted_N = stacking_model_N.predict(input)[0]
    except Exception as e:
        print(f"An error occurred: {e}")

    predicted_P = stacking_model_P.predict(input)[0]
    predicted_K = stacking_model_K.predict(input)[0]
    def calculate_deficiency(predicted, actual):
        return max(0, predicted - actual)

    # Calculate deficiencies
    deficient_N = calculate_deficiency(predicted_N, N)
    deficient_P = calculate_deficiency(predicted_P, P)
    deficient_K = calculate_deficiency(predicted_K, K)


    # Available fertilizers (in Ethiopia): Urea=60% Nitrogen, DAP=18% Nitrogen and 60% Phosphorus, MOP=60% Potassium
    MOP = 0
    DAP = 0
    Urea = 0

    # Recommend MOP if there is K deficiency
    if deficient_K > 0:
        MOP = deficient_K / 0.6
        
    # Recommend DAP if there is P deficiency
    if deficient_P > 0:
        DAP = deficient_P / 0.6
        # Calculate remaining Nitrogen deficiency after applying DAP
        remaining_deficient_N = max(0, deficient_N - (DAP * 0.18))
    else:
        remaining_deficient_N = deficient_N

    # Recommend Urea
    if remaining_deficient_N > 0 :
         Urea = remaining_deficient_N / 0.6 

    return (f"We recommend you add {MOP:.2f}kgs of MOP, {DAP:.2f}kgs of DAP and, {Urea:.2f}kgs of Urea.")



def main():
    st.title("Fertilizer Recommender")
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Streamlit Fertilizer Recommender ML App </h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)

    N_amount = st.number_input('Enter N_amount', step=0.000000000000001)
    P_amount = st.number_input('P_amount', step=0.000000000000001)
    K_amount = st.number_input('K_amount', step=0.000000000000001)
    temperature = st.number_input('Temperature', step=0.000000000000001)
    humidity = st.number_input('Humidity', step=0.000000000000001)
    ph = st.number_input('Ph', step=0.000000000000001)
    rainfall = st.number_input('rainfall', step=0.000000000000001)
    label = st.number_input('Type of Crop')
    result=""
    if st.button("Predict"):
        result=predict__amount_of_fertilizer(N_amount, P_amount, K_amount, temperature, humidity, ph, rainfall, label)
    st.success('The output is {}'.format(result))
    if st.button("About"):
        st.text("Lets LEarn")
        st.text("Built with Streamlit")

if name=='main':
    main()