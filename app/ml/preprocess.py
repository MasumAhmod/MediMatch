from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


# Dataset Paths
BASE_DIR = Path(__file__).parent
DATASET_DIR = BASE_DIR / "datasets"

DOCTOR_DATA_PATH = DATASET_DIR / "DoctorData.csv"
PATIENT_DATA_PATH = DATASET_DIR / "PatientData.csv"


def load_data():
    """
    Load doctor and patient datasets.
    """

    doctorData = pd.read_csv(DOCTOR_DATA_PATH)
    PatientData = pd.read_csv(PATIENT_DATA_PATH)

    # Remove unnecessary column if it exists
    if "Unnamed: 10" in doctorData.columns:
        doctorData.drop(columns=["Unnamed: 10"], inplace=True)

    return doctorData, PatientData


def preprocess_patient_data(PatientData):
    """
    Split patient dataset into training and testing sets.
    """

    X = PatientData.drop(columns=["diseases"])
    y = PatientData["diseases"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    return X_train, X_test, y_train, y_test