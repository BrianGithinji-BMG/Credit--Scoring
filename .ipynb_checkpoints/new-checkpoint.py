import streamlit as st

# Function to calculate credit score
def calculate_credit_score(inputs):
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
    income_normalized = (inputs["Avg_Income"] / 30000) * 100
    yield_normalized = (inputs["Yield_Efficiency"] / 2000) * 100
    
    # Calculate scores
    experience_score = (
        inputs["Crop_Management"] * weights["Crop_Management"] +
        income_normalized * weights["Income"] +
        yield_normalized * weights["Yield_Efficiency"] +
        inputs["Record_Keeping"] * weights["Record_Keeping"]
    )
    
    farm_details_score = (
        (inputs["Active_Land"] / inputs["Farm_Size"]) * 100 * weights["Farm_Size"] +
        inputs["Crop_Type_Score"] * weights["Crop_Type_Score"] +
        inputs["Irrigation_Score"] * weights["Irrigation_Score"]
    )
    
    weather_risk_contribution = (100 - inputs["Weather_Risk"]) * weights["Weather_Risk"]
    farm_inputs_contribution = inputs["Farm_Inputs"] * weights["Farm_Inputs"]
    
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
st.write("Enter your farming details to calculate your credit score.")

# Input form
with st.form("farmer_input_form"):
    st.header("Farmer Details")
    crop_management = st.slider("Crop Management Score (0-100)", 0, 100, 50)
    avg_income = st.number_input("Average Annual Income (USD)", min_value=0, max_value=30000, value=10000)
    yield_efficiency = st.number_input("Yield Efficiency (kg/acre)", min_value=0, max_value=2000, value=1000)
    record_keeping = st.slider("Record Keeping Score (0-100)", 0, 100, 50)
    farm_size = st.number_input("Total Farm Size (acres)", min_value=1, max_value=20, value=5)
    active_land = st.number_input("Active Land (acres)", min_value=1, max_value=20, value=5)
    crop_type_score = st.selectbox("Crop Type Score", [65, 70, 75, 78, 80], index=0)
    irrigation_score = st.slider("Irrigation Score (0-100)", 0, 100, 50)
    farm_inputs = st.slider("Farm Inputs Score (0-100)", 0, 100, 50)
    weather_risk = st.slider("Weather Risk Score (0-100)", 0, 100, 50)
    
    submitted = st.form_submit_button("Calculate Credit Score")

# Calculate and display credit score
if submitted:
    inputs = {
        "Crop_Management": crop_management,
        "Avg_Income": avg_income,
        "Yield_Efficiency": yield_efficiency,
        "Record_Keeping": record_keeping,
        "Farm_Size": farm_size,
        "Active_Land": active_land,
        "Crop_Type_Score": crop_type_score,
        "Irrigation_Score": irrigation_score,
        "Farm_Inputs": farm_inputs,
        "Weather_Risk": weather_risk,
    }
    
    credit_score = calculate_credit_score(inputs)
    
    # Determine risk tier
    if credit_score <= 50:
        risk_tier = "High Risk (C)"
    elif 50 < credit_score <= 70:
        risk_tier = "Medium Risk (B)"
    else:
        risk_tier = "Low Risk (A)"
    
    # Display results
    st.success(f"Your Credit Score: **{credit_score:.1f}%**")
    st.success(f"Risk Tier: **{risk_tier}**")