import sqlite3
from datetime import datetime
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

def init_db():
    conn = sqlite3.connect("predictions.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS history (time TEXT, tenure INTEGER, monthly_charges REAL, churn_pred TEXT, revenue REAL)")
    conn.commit()
    conn.close()

def save_prediction(tenure, monthly, churn, revenue):
    conn = sqlite3.connect("predictions.db")
    c = conn.cursor()
    c.execute("INSERT INTO history VALUES(?,?,?,?,?)",(datetime.now().strftime("%d-%m %H:%M"),tenure, monthly, churn, revenue))
    conn.commit()
    conn.close()

init_db()



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

    churn_label = "HIGH" if churn_prob > 0.5 else "MEDIUM" if churn_prob > 0.3 else "LOW"
    save_prediction(tenure,monthly_charges,churn_label,monthly_charges*12)
    st.toast("Prediction Database me save ho gaya! ✅")

else:
    st.info("👈 Sidebar me deatails bharke 'Predict Churn' pe click karo.")

    st.markdown("### Dashboard Insights:")


st.sidebar.divider()
if st.sidebar.checkbox("Show Prediction History"):
    conn = sqlite3.connect("predictions.db")
    c = conn.cursor()
    c.execute("SELECT * FROM history ORDER BY time DESC")
    data = c.fetchall()
    conn.close()

    import pandas as pd
    df_hist = pd.DataFrame(data, columns=["Time", "Tenure", "Monthly", "Churn", "Revenue"])
    st.subheader("📃 Past Predictions History")
    st.dataframe(df_hist, use_container_width=True)
    



