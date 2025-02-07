import streamlit as st
import pandas as pd
import numpy as np

# ================================
# 💄 Custom CSS Styling
# ================================
st.markdown(
    """
    <style>
        .stApp { background-color: #f4f4f4; }
        h1 { color: #6a0dad; text-align: center; font-size: 35px; font-weight: bold; }
        .stButton > button {
            background-color: #6a0dad; color: white; border-radius: 8px;
            width: 100%; font-size: 18px; padding: 10px;
        }
        .stButton > button:hover { background-color: #500b79; }
        .stAlert { background-color: #eaf4ea; border-left: 5px solid #34a853;
                   color: black; padding: 10px; font-size: 18px; }
    </style>
    """,
    unsafe_allow_html=True
)

# ================================
# 🎯 Title & Subtitle
# ================================
st.title("🌱 SOWPHIE - Smart Credit Scoring for Farmers")
st.markdown("### 📊 Enter your details below to calculate your **credit score**.")

# ================================
# 📩 User Input Form
# ================================
with st.form("user_input_form"):
    st.subheader("👤 Demographic Information")
    age = st.slider("📌 Age", 18, 70, 30)
    marital_status = st.selectbox("📌 Marital Status", ["Single", "Married", "Divorced", "Widowed"])
    education_level = st.selectbox("📌 Education Level", ["None", "Primary School", "Secondary School", "Higher Education"])
    farming_experience = st.slider("📌 Farming Experience (Years)", 0, 40, 5)
    sacco_membership = st.selectbox("📌 SACCO Membership", ["No", "Yes"])

    st.subheader("💰 Financial Information")
    annual_income = st.number_input("📌 Annual Income (KES)", min_value=50000, max_value=5000000, step=10000)
    loan_amount = st.number_input("📌 Loan Amount (KES)", min_value=10000, max_value=1000000, step=5000)
    loan_to_income_ratio = loan_amount / annual_income if annual_income != 0 else 0
    savings_contributions = st.number_input("📌 Annual Savings (KES)", min_value=1000, max_value=500000, step=5000)

    st.subheader("📜 Loan Details")
    loan_purpose = st.selectbox("📌 Loan Purpose", ["Farm Expansion", "Machinery Purchase", "Farm Inputs", "Labor Costs", "Harvesting Costs", "Debt Consolidation", "Personal Use"])
    repayment_history = st.selectbox("📌 Repayment History", ["Good", "Fair", "Poor"])

    st.subheader("📊 External Factors & Market Data")
    sacco_frequency = st.selectbox("📌 SACCO Contribution Frequency", ["Annually", "Semi-Annually", "Monthly"])
    weather_risks = st.selectbox("📌 Weather Risks", ["High", "Moderate", "Low"])

    # Submit button
    submit_button = st.form_submit_button("🚀 Calculate Credit Score")

# ================================
# 🧮 Scoring Functions
# ================================
def score_age(age): return 2 if age <= 25 else 5 if age <= 40 else 4 if age <= 60 else 2
def score_marital_status(status): return {"Single": 2, "Married": 4, "Divorced": 1, "Widowed": 1}.get(status, 0)
def score_education(level): return {"None": 1, "Primary School": 2, "Secondary School": 3, "Higher Education": 7}.get(level, 0)
def score_farming_experience(years): return 2 if years <= 2 else 4 if years <= 5 else 6 if years <= 10 else 7
def score_sacco_membership(status): return {"No": 0, "Yes": 5}.get(status, 0)
def score_annual_income(income): return 1 if income < 200_000 else 3 if income <= 1_000_000 else 5
def score_loan_to_income_ratio(ratio): return 1 if ratio > 0.70 else 3 if ratio >= 0.31 else 5
def score_savings_contributions(amount): return 1 if amount < 10_000 else 3 if amount <= 50_000 else 5
def score_loan_amount(amount): return 0.5 if amount > 1_000_000 else 0.75 if amount > 500_000 else 1
def score_repayment_history(history): return {"Good": 2, "Fair": 1, "Poor": 0.5}.get(history, 0)
def score_sacco_contribution_frequency(freq): return {"Annually": 1, "Semi-Annually": 2, "Monthly": 3}.get(freq, 0)
def score_weather_risks(exposure): return {"High": 1, "Moderate": 2, "Low": 3}.get(exposure, 0)

# ================================
# 🎯 Weighted Score Calculation
# ================================
weights = {
    "Demographic": 21.06, "Financial": 25, "Loan Details": 10,
    "Credit History": 10, "Behavioral": 7.89, "External Factors": 5.53, "Farm Data": 28.96, "Market Data": 6.32
}

def calculate_credit_score(user_data):
    scores = {
        "Age Score": score_age(user_data["Age"]),
        "Marital Score": score_marital_status(user_data["Marital Status"]),
        "Education Score": score_education(user_data["Education Level"]),
        "Farming Exp Score": score_farming_experience(user_data["Farming Experience"]),
        "Sacco Score": score_sacco_membership(user_data["SACCO Membership"]),
        "Income Score": score_annual_income(user_data["Annual Income"]),
        "Loan-to-Income Score": score_loan_to_income_ratio(user_data["Loan-To-Income Ratio"]),
        "Savings Score": score_savings_contributions(user_data["Savings Contributions"]),
        "Loan Amount Score": score_loan_amount(user_data["Loan Amount"]),
        "Repayment Score": score_repayment_history(user_data["Repayment History"]),
        "Sacco Frequency Score": score_sacco_contribution_frequency(user_data["SACCO Contribution Frequency"]),
        "Weather Risk Score": score_weather_risks(user_data["Weather Risks"]),
    }

    total_score = (
        (sum([scores[key] for key in ["Age Score", "Marital Score", "Education Score", "Farming Exp Score", "Sacco Score"]]) / 28) * weights["Demographic"] +
        (sum([scores[key] for key in ["Income Score", "Loan-to-Income Score", "Savings Score"]]) / 15) * weights["Financial"] +
        (scores["Loan Amount Score"] / 10) * weights["Loan Details"] +
        (scores["Repayment Score"] / 5) * weights["Credit History"] +
        (scores["Sacco Frequency Score"] / 10) * weights["Behavioral"] +
        (scores["Weather Risk Score"] / 5) * weights["External Factors"]
    )

    normalized_score = round(total_score, 2)
    return normalized_score

# ================================
# ✅ Display Credit Score
# ================================
if submit_button:
    user_data = {
        "Age": age, "Marital Status": marital_status, "Education Level": education_level,
        "Farming Experience": farming_experience, "SACCO Membership": sacco_membership,
        "Annual Income": annual_income, "Loan Amount": loan_amount, "Loan-To-Income Ratio": loan_to_income_ratio,
        "Savings Contributions": savings_contributions, "Repayment History": repayment_history,
        "SACCO Contribution Frequency": sacco_frequency, "Weather Risks": weather_risks
    }

    score = calculate_credit_score(user_data)
    st.success(f"✅ Your Estimated Credit Score: **{score}%**")


