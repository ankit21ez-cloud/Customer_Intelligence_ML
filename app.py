import streamlit as st
import pickle
import pandas as pd

st.set_page_config(
    page_title="Customer Intelligence ML",
    page_icon="📊",
    layout="wide"
)
@st.cache_resource
def load_model():
    try:
        with open("churn_model.pkl","rb") as f:
            model = pickle.load(f)
        return model
    except:
        return None

model = load_model()

st.title("📊 Customer Intelligence - Churn Prediction")
st.markdown("### Revenue & Churn Prediction Dashboard")

st.sidebar.header("Customer Details")

tenure = st.sidebar.slider("Tenure (Months)",0,72,12)
monthly_charges = st.sidebar.number_input("Monthly Charges ($)", 18.0, 120.0, 64.76)
total_charges = st.sidebar.number_input("Total Charges ($)", 0.0, 10000.0, 1500.0)

contract = st.sidebar.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
payment = st.sidebar.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
internet = st.sidebar.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
online_security = st.sidebar.selectbox("Online Security", ["Yes", "No"])


if st.sidebar.button("Predict Churn"):

    
    churn_prob = 0.27
    if contract == "Month-to-month":
        churn_prob += 0.15
    if payment == "Electronic check":
        churn_prob += 0.08
    if internet == "Fiber optic":
        churn_prob += 0.05

    churn_prob = min(churn_prob, 0.99)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Churn Probability", f"{churn_prob:.2f}")
    col2.metric("Avg Monthly Charges", f"${monthly_charges}")
    col3.metric("Total Revenue", "$16.06M")
    col4.metric("Revenue at Risk", f"${monthly_charges * churn_prob:.2f}")

    st.divider()

    if churn_prob > 0.5:
        st.error(f"⚠️ HIGH RISK: Customer ke churn karne ka chance {churn_prob*100:.0f}% hai!")
        st.write("**Recommendation:** Is customer ko One/Two year contract offer karo + discount do.")
    elif churn_prob > 0.3:
        st.warning(f"⚠️ MEDIUM RISK: Churn chance {churn_prob*100:.0f}% hai - dhyan dene ki zarurat hai")
    else:
        st.success(f"✅ LOW RISK: Customer safe hai - Churn chance {churn_prob*100:.0f}%")


else:
    st.info("👈 Sidebar me deatails bharke 'Predict Churn' pe click karo.")

    st.markdown("### Dashboard Insights:")



