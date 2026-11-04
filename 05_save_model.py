import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

df = pd.read_csv(r"C:\Users\ANKIT KASHYAP\Desktop\Customer_Intelligence_ML\dataset\WA_Fn-UseC_-Telco-Customer-Churn.csv")
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"],errors="coerce")
df["TotalCharges"] = df["TotalCharges"].fillna(0)
df = df.drop("customerID",axis=1)
df["Churn"] = df["Churn"].map({"Yes":1,"No":0})
df = df.dropna()
df = pd.get_dummies(df,drop_first=True)

x = df.drop("Churn",axis=1)
y = df["Churn"]
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(x_train,y_train)

with open("churn_model.pkl","wb") as f:
    pickle.dump(model,f)

print("Model save as churn_model.pkl")