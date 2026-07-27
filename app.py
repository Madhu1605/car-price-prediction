import streamlit as st
import pandas as pd
import pickle

# Load model files

model = pickle.load(open("car.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

st.set_page_config(page_title="Car Price Prediction", page_icon="🚗")

st.title("🚗 Ford Car Price Prediction")

# Extract dropdown values

model_list = sorted(
    [c.replace("model_ ", "") for c in columns if c.startswith("model_ ")]
)

fuel_list = sorted(
    [c.replace("fuelType_", "") for c in columns if c.startswith("fuelType_")]
)

transmission_list = sorted(
    [c.replace("transmission_", "") for c in columns if c.startswith("transmission_")]
)

# Add dropped categories (drop_first=True)

if "Petrol" not in fuel_list:
    fuel_list.insert(0, "Petrol")

if "Automatic" not in transmission_list:
    transmission_list.insert(0, "Automatic")

# User Inputs

model_name = st.selectbox("Model", model_list)

year = st.number_input(
    "Year",
    min_value=1996,
    max_value=2025,
    value=2018
)

mileage = st.number_input(
    "Mileage",
    min_value=0,
    value=20000
)

tax = st.number_input(
    "Tax",
    min_value=0,
    value=145
)

mpg = st.number_input(
    "MPG",
    min_value=0.0,
    value=55.4
)

engine = st.number_input(
    "Engine Size",
    min_value=0.0,
    value=1.2
)

fuel = st.selectbox(
    "Fuel Type",
    fuel_list
)

transmission = st.selectbox(
    "Transmission",
    transmission_list
)

# Prediction

if st.button("Predict Price"):

    # Create dataframe
    input_df = pd.DataFrame(0, index=[0], columns=columns)

    input_df["year"] = year
    input_df["mileage"] = mileage
    input_df["tax"] = tax
    input_df["mpg"] = mpg
    input_df["engineSize"] = engine

    model_col = "model_ " + model_name
    fuel_col = "fuelType_" + fuel
    transmission_col = "transmission_" + transmission

    if model_col in input_df.columns:
        input_df[model_col] = 1

    if fuel_col in input_df.columns:
        input_df[fuel_col] = 1

    if transmission_col in input_df.columns:
        input_df[transmission_col] = 1

    num_cols = ["year", "mileage", "tax", "mpg", "engineSize"]
    input_df[num_cols] = scaler.transform(input_df[num_cols])

    prediction = model.predict(input_df)[0]

    st.success(f"💰 Estimated Car Price: £{prediction:,.2f}")