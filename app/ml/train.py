from __future__ import annotations
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import argparse
from pathlib import Path
import pandas as pd

doctorData = pd.read_csv(
    r"C:\Users\HP\OneDrive\Desktop\MediMatch\app\ml\datasets\DoctorData.csv"
)

PatientData = pd.read_csv(
    r"C:\Users\HP\OneDrive\Desktop\MediMatch\app\ml\datasets\PatientData.csv"
)
doctorData.drop(columns=['Unnamed: 10'], inplace=True)

X = PatientData.drop("diseases", axis=1)
y = PatientData["diseases"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Decision Tree Classifier
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)

# Random Forest Classifier
rf = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)
rf.fit(X_train, y_train)

#Logistic Regression Classifier
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)

# Evaluate the models
pred = dt.predict(X_test)
# print(f"Decision Tree Accuracy: {accuracy_score(y_test, pred)}")

pred = rf.predict(X_test)
# print(f"Random Forest Accuracy: {accuracy_score(y_test, pred)}")

pred = lr.predict(X_test)
# print(f"Logistic Regression Accuracy: {accuracy_score(y_test, pred)}")

#report
# print(classification_report(y_test, pred))

models = {
    "Decision Tree": dt,
    "Random Forest": rf,
    "Logistic Regression": lr
}

results = []

for name, model in models.items():

    pred = model.predict(X_test)

    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, pred),
        "Precision": precision_score(y_test, pred, average="weighted"),
        "Recall": recall_score(y_test, pred, average="weighted"),
        "F1-score": f1_score(y_test, pred, average="weighted")
    })

results_df = pd.DataFrame(results)

print(results_df)