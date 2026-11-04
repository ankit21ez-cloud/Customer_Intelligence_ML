import pandas as pd
df = pd.read_csv(r"C:\Users\ANKIT KASHYAP\Desktop\Customer_Intelligence_ML\dataset\WA_Fn-UseC_-Telco-Customer-Churn.csv")
print(df.head())
print(df.columns)
print(df.describe())
print(df.shape)
print(df.info())
print(df.isnull().sum())
print("duplicated row :",df.duplicated().sum())
print("duplicated customer id :",df["customerID"].duplicated().sum())
print("TotalCharges :",(df["TotalCharges"].str.strip()=="").sum())
print("data type :",df["TotalCharges"].dtype)

df["TotalCharges"] = df["TotalCharges"].str.strip()
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"],errors="coerce")

print("data type :",df["TotalCharges"].dtype)
print("Missing values :",df["TotalCharges"].isnull().sum())

missing_val = df[df["TotalCharges"].isnull()]
print("missing_val :",missing_val[["customerID","tenure","MonthlyCharges","TotalCharges"]])

df["TotalCharges"] = df["TotalCharges"].fillna(0)

print("Fill karne ke bad Missing vaalue :",df["TotalCharges"].isnull().sum())
print("Data typee :",df["TotalCharges"].dtype)