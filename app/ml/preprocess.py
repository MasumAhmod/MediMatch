from sklearn.model_selection import train_test_split
import pandas as pd

DOCTOR_DATA_PATH = r"C:\Users\HP\OneDrive\Desktop\MediMatch\app\ml\datasets\DoctorData.csv"
PATIENT_DATA_PATH = r"C:\Users\HP\OneDrive\Desktop\MediMatch\app\ml\datasets\PatientData.csv"


def load_data():

    doctorData = pd.read_csv(DOCTOR_DATA_PATH)
    PatientData = pd.read_csv(PATIENT_DATA_PATH)

    doctorData.drop(columns=["Unnamed: 10"], inplace=True)

    return doctorData, PatientData


def preprocess_patient_data(PatientData):

    X = PatientData.drop("diseases", axis=1)
    y = PatientData["diseases"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    return X_train, X_test, y_train, y_test