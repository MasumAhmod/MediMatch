from __future__ import annotations

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
print(PatientData.duplicated().sum())