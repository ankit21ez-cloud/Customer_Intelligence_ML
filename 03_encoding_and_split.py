import pandas as pd

df = pd.read_csv(r"C:\Users\ANKIT KASHYAP\Desktop\Customer_Intelligence_ML\dataset\WA_Fn-UseC_-Telco-Customer-Churn.csv")
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"],errors="coerce")
df["TotalCharges"] = df["TotalCharges"].fillna(0)
df = df.drop("customerID",axis=1)

df["Churn"] = df["Churn"].map({"Yes":1,"No":0})

df = pd.get_dummies(df,drop_first=True)

print("Encoding ke baad shape :",df.shape)
print(df.head())

x = df.drop("Churn",axis=1)
y = df["Churn"]
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)
print(f"Train:{x_train.shape}, Test:{x_test.shape}")
print("done ! Ab model banane ke liye ready hai")

