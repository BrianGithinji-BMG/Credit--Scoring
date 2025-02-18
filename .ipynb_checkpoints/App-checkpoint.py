import streamlit as st
import pandas as pd
import numpy as np

# Load synthetic data
@st.cache
def load_data():
    return pd.read_csv("synthetic_farmers_data.csv")

# Calculate credit score
def calculate_credit_score(row):
    weights = {
        "Crop_Management": 0.3,
        "Income": 0.25,
        "Yield_Efficiency": 0.25,
        "Record_Keeping": 0.2,
        "Farm_Size": 0.4,
        "Crop_Type_Score": 0.3,
        "Irrigation_Score": 0.3,
        "Weather_Risk": 0.2,
        "Farm_Inputs": 0.1,
    }
    
    # Normalize income and yield
    income_normalized = (row["Avg_Income"] / 30000) * 100
    yield_normalized = (row["Yield_Efficiency"] / 2000) * 100
    
    # Calculate scores
    experience_score = (
        row["Crop_Management"] * weights["Crop_Management"] +
        income_normalized * weights["Income"] +
        yield_normalized * weights["Yield_Efficiency"] +
        row["Record_Keeping"] * weights["Record_Keeping"]
    )
    
    farm_details_score = (
        (row["Active_Land"] / row["Farm_Size"]) * 100 * weights["Farm_Size"] +
        row["Crop_Type_Score"] * weights["Crop_Type_Score"] +
        row["Irrigation_Score"] * weights["Irrigation_Score"]
    )
    
    weather_risk_contribution = (100 - row["Weather_Risk"]) * weights["Weather_Risk"]
    farm_inputs_contribution = row["Farm_Inputs"] * weights["Farm_Inputs"]
    
    # Total credit score (0-100%)
    credit_score = (
        experience_score * 0.4 +
        farm_details_score * 0.3 +
        weather_risk_contribution * 0.2 +
        farm_inputs_contribution * 0.1
    )
    
    return credit_score

# Streamlit app
st.title("Farmer Credit Scoring App")
st.write("Upload farmer data to calculate credit scores.")

# Upload data
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Uploaded Data:")
    st.write(data.head())
    
    # Calculate credit scores
    data["Credit_Score_Percentage"] = data.apply(calculate_credit_score, axis=1)
    data["Risk_Tier"] = pd.cut(
        data["Credit_Score_Percentage"],
        bins=[0, 50, 70, 100],
        labels=["High Risk (C)", "Medium Risk (B)", "Low Risk (A)"]
    )
    
    st.write("Credit Scores:")
    st.write(data[["Farmer_ID", "Credit_Score_Percentage", "Risk_Tier"]])
    
    # Download results
    st.download_button(
        label="Download Credit Scores",
        data=data.to_csv(index=False).encode("utf-8"),
        file_name="credit_scores.csv",
        mime="text/csv",
    )