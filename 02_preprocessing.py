import pandas as pd
df = pd.read_csv(r"C:\Users\ANKIT KASHYAP\Desktop\Customer_Intelligence_ML\dataset\WA_Fn-UseC_-Telco-Customer-Churn.csv")
df["TotalCharges"] = df["TotalCharges"].str.strip()
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"],errors="coerce")
df["TotalCharges"] = df["TotalCharges"].fillna(0)

df = df.drop("customerID",axis=1)

df["Churn"]= df["Churn"].map({"Yes":1,"No":0})

print("Shape after droping ID :",df.shape)
print(df["Churn"].value_counts())
print(df.head(2))