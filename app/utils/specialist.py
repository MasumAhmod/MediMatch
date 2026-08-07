"""
MediMatch Specialist Utility

Converts predicted diseases into appropriate medical specializations.

The disease is predicted by the ML model, and this module determines
which type of specialist should handle that disease.

No additional database table is required.
"""


# ---------------------------------------------------------
# Disease -> Specialization mapping
# ---------------------------------------------------------

DISEASE_SPECIALIST_MAP = {

    # -------------------------
    # Cardiology
    # -------------------------
    "heart attack": "Cardiology",
    "myocardial infarction": "Cardiology",
    "coronary artery disease": "Cardiology",
    "heart failure": "Cardiology",
    "angina": "Cardiology",
    "cardiac arrhythmia": "Cardiology",
    "atrial fibrillation": "Cardiology",
    "hypertension": "Cardiology",

    # -------------------------
    # Neurology
    # -------------------------
    "migraine": "Neurology",
    "epilepsy": "Neurology",
    "seizure": "Neurology",
    "parkinson disease": "Neurology",
    "multiple sclerosis": "Neurology",
    "stroke": "Neurology",
    "dementia": "Neurology",
    "neuropathy": "Neurology",

    # -------------------------
    # Dermatology
    # -------------------------
    "acne": "Dermatology",
    "eczema": "Dermatology",
    "psoriasis": "Dermatology",
    "dermatitis": "Dermatology",
    "skin infection": "Dermatology",
    "skin rash": "Dermatology",
    "urticaria": "Dermatology",

    # -------------------------
    # Gastroenterology
    # -------------------------
    "gastritis": "Gastroenterology",
    "peptic ulcer": "Gastroenterology",
    "ulcerative colitis": "Gastroenterology",
    "crohn disease": "Gastroenterology",
    "irritable bowel syndrome": "Gastroenterology",
    "gastroesophageal reflux disease": "Gastroenterology",
    "hepatitis": "Gastroenterology",

    # -------------------------
    # Pulmonology
    # -------------------------
    "asthma": "Pulmonology",
    "pneumonia": "Pulmonology",
    "bronchitis": "Pulmonology",
    "chronic obstructive pulmonary disease": "Pulmonology",
    "copd": "Pulmonology",
    "tuberculosis": "Pulmonology",

    # -------------------------
    # ENT
    # -------------------------
    "otitis externa (swimmer's ear)": "ENT",
    "otitis media": "ENT",
    "sinusitis": "ENT",
    "tonsillitis": "ENT",
    "pharyngitis": "ENT",
    "laryngitis": "ENT",

    # -------------------------
    # Ophthalmology
    # -------------------------
    "conjunctivitis": "Ophthalmology",
    "cataract": "Ophthalmology",
    "glaucoma": "Ophthalmology",
    "retinal disorder": "Ophthalmology",

    # -------------------------
    # Orthopedics
    # -------------------------
    "arthritis": "Orthopedics",
    "osteoarthritis": "Orthopedics",
    "rheumatoid arthritis": "Rheumatology",
    "fracture": "Orthopedics",
    "osteoporosis": "Orthopedics",
    "back pain": "Orthopedics",

    # -------------------------
    # Urology
    # -------------------------
    "urinary tract infection": "Urology",
    "kidney stone": "Urology",
    "kidney stones": "Urology",
    "prostatitis": "Urology",
    "benign prostatic hyperplasia": "Urology",

    # -------------------------
    # Gynecology
    # -------------------------
    "endometriosis": "Gynecology",
    "ovarian cyst": "Gynecology",
    "polycystic ovary syndrome": "Gynecology",
    "pcos": "Gynecology",

    # -------------------------
    # Psychiatry
    # -------------------------
    "depression": "Psychiatry",
    "anxiety disorder": "Psychiatry",
    "bipolar disorder": "Psychiatry",
    "schizophrenia": "Psychiatry",
    "panic disorder": "Psychiatry",

    # -------------------------
    # Endocrinology
    # -------------------------
    "diabetes": "Endocrinology",
    "diabetes mellitus": "Endocrinology",
    "hypothyroidism": "Endocrinology",
    "hyperthyroidism": "Endocrinology",
}


# ---------------------------------------------------------
# Keyword based fallback
# ---------------------------------------------------------

SPECIALIST_KEYWORDS = {

    "cardio": "Cardiology",
    "heart": "Cardiology",
    "hypertension": "Cardiology",

    "brain": "Neurology",
    "neuro": "Neurology",
    "migraine": "Neurology",
    "seizure": "Neurology",

    "skin": "Dermatology",
    "acne": "Dermatology",
    "eczema": "Dermatology",

    "stomach": "Gastroenterology",
    "gastric": "Gastroenterology",
    "intestinal": "Gastroenterology",
    "liver": "Gastroenterology",

    "lung": "Pulmonology",
    "pulmonary": "Pulmonology",
    "asthma": "Pulmonology",
    "pneumonia": "Pulmonology",

    "ear": "ENT",
    "nose": "ENT",
    "throat": "ENT",
    "sinus": "ENT",

    "eye": "Ophthalmology",
    "vision": "Ophthalmology",
    "retina": "Ophthalmology",

    "bone": "Orthopedics",
    "joint": "Orthopedics",
    "fracture": "Orthopedics",
    "muscle": "Orthopedics",

    "kidney": "Urology",
    "urinary": "Urology",
    "prostate": "Urology",

    "pregnancy": "Gynecology",
    "ovary": "Gynecology",
    "uterus": "Gynecology",

    "depression": "Psychiatry",
    "anxiety": "Psychiatry",
    "psychotic": "Psychiatry",

    "diabetes": "Endocrinology",
    "thyroid": "Endocrinology",
}


# ---------------------------------------------------------
# Main function
# ---------------------------------------------------------

def get_specialization(disease: str) -> str:
    """
    Return the most appropriate medical specialization
    for a predicted disease.
    """

    if not disease:
        return "General Medicine"

    disease_normalized = disease.strip().lower()

    # Exact match
    if disease_normalized in DISEASE_SPECIALIST_MAP:
        return DISEASE_SPECIALIST_MAP[disease_normalized]

    # Keyword fallback
    for keyword, specialization in SPECIALIST_KEYWORDS.items():

        if keyword in disease_normalized:
            return specialization

    # Default
    return "General Medicine"