import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load the model and data
pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))

# Customizing the title and layout
st.set_page_config(page_title="Laptop Price Predictor", page_icon="💻", layout="wide")
st.title("💻 Laptop Price Predictor")
st.markdown("### Predict the price of a laptop with ease by filling out the details below!")

# Group inputs into categories using columns for better UI
st.sidebar.title("Input Features")
st.sidebar.markdown("### Select the specifications of the laptop:")
company = st.sidebar.selectbox('Brand', df['Company'].unique())
type_name = st.sidebar.selectbox('Type', df['TypeName'].unique())
ram = st.sidebar.selectbox('RAM (in GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64])
weight = st.sidebar.number_input('Weight (kg)', min_value=0.1, max_value=10.0, value=2.0, step=0.1)
touchscreen = st.sidebar.selectbox('Touchscreen', ['No', 'Yes'])
ips = st.sidebar.selectbox('IPS Display', ['No', 'Yes'])
screen_size = st.sidebar.slider('Screen Size (inches)', 10.0, 18.0, 13.0)
resolution = st.sidebar.selectbox('Screen Resolution', [
    '1920x1080', '1366x768', '1600x900', '3840x2160', 
    '3200x1800', '2880x1800', '2560x1600', '2560x1440', '2304x1440'
])
cpu = st.sidebar.selectbox('CPU', df['Cpu brand'].unique())
hdd = st.sidebar.selectbox('HDD (in GB)', [0, 128, 256, 512, 1024, 2048])
ssd = st.sidebar.selectbox('SSD (in GB)', [0, 8, 128, 256, 512, 1024])
gpu = st.sidebar.selectbox('GPU', df['Gpu brand'].unique())
os = st.sidebar.selectbox('Operating System', df['os'].unique())

# Function to calculate PPI
def calculate_ppi(resolution, screen_size):
    try:
        x_res, y_res = map(int, resolution.split('x'))
        return ((x_res**2) + (y_res**2))**0.5 / screen_size
    except:
        return 0  # default value if calculation fails

if st.sidebar.button("Predict Price"):
    # Process inputs
    touchscreen = 1 if touchscreen == 'Yes' else 0
    ips_value = 1 if ips == 'Yes' else 0
    ppi = calculate_ppi(resolution, screen_size)
    
    # Create a DataFrame with the correct feature names
    query = pd.DataFrame({
        'Company': [company],
        'TypeName': [type_name],
        'Ram': [ram],
        'Weight': [weight],
        'Touchscreen': [touchscreen],
        'Ips': [ips_value],
        'ppi': [ppi],
        'Cpu brand': [cpu],
        'HDD': [hdd],
        'SSD': [ssd],
        'Gpu brand': [gpu],
        'os': [os]
    })
    
    # Make prediction
    try:
        pred = np.exp(pipe.predict(query)[0])
        formatted_price = f"₹{pred:,.2f}"
        st.success(f"The predicted price is: **{formatted_price}**")
    except Exception as e:
        st.error("An error occurred during prediction.")
        st.write(f"Details: {e}")