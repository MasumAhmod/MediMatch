import re
import spacy


# =========================================================
# LOAD SPACY MODEL
# =========================================================

nlp = spacy.load("en_core_web_sm")


# =========================================================
# DATASET SYMPTOMS
# These names must match PatientData.csv exactly
# =========================================================

SYMPTOMS = [
    "anxiety and nervousness",
    "depression",
    "shortness of breath",
    "depressive or psychotic symptoms",
    "sharp chest pain",
    "dizziness",
    "insomnia",
    "abnormal involuntary movements",
    "chest tightness",
    "palpitations",
    "irregular heartbeat",
    "breathing fast",
    "hoarse voice",
    "sore throat",
    "difficulty speaking",
    "cough",
    "nasal congestion",
    "throat swelling",
    "diminished hearing",
    "difficulty in swallowing",
    "skin swelling",
    "retention of urine",
    "leg pain",
    "hip pain",
    "suprapubic pain",
    "blood in stool",
    "lack of growth",
    "symptoms of the scrotum and testes",
    "swelling of scrotum",
    "pain in testicles",
    "pus draining from ear",
    "jaundice",
    "white discharge from eye",
    "irritable infant",
    "abusing alcohol",
    "fainting",
    "hostile behavior",
    "drug abuse",
    "sharp abdominal pain",
    "feeling ill",
    "vomiting",
    "headache",
    "nausea",
    "diarrhea",
    "vaginal itching",
    "painful urination",
    "involuntary urination",
    "pain during intercourse",
    "frequent urination",
    "lower abdominal pain",
    "vaginal discharge",
    "blood in urine",
    "hot flashes",
    "intermenstrual bleeding",
    "hand or finger pain",
    "wrist pain",
    "hand or finger swelling",
    "arm pain",
    "wrist swelling",
    "arm stiffness or tightness",
    "arm swelling",
    "hand or finger stiffness or tightness",
    "lip swelling",
    "toothache",
    "abnormal appearing skin",
    "skin lesion",
    "acne or pimples",
    "facial pain",
    "mouth ulcer",
    "skin growth",
    "diminished vision",
    "double vision",
    "symptoms of eye",
    "pain in eye",
    "abnormal movement of eyelid",
    "foreign body sensation in eye",
    "irregular appearing scalp",
    "back pain",
    "neck pain",
    "low back pain",
    "pain of the anus",
    "pain during pregnancy",
    "pelvic pain",
    "impotence",
    "vomiting blood",
    "regurgitation",
    "burning abdominal pain",
    "restlessness",
    "wheezing",
    "peripheral edema",
    "neck mass",
    "ear pain",
    "jaw swelling",
    "mouth dryness",
    "neck swelling",
    "knee pain",
    "foot or toe pain",
    "ankle pain",
    "bones are painful",
    "elbow pain",
    "knee swelling",
    "skin moles",
    "weight gain",
    "problems with movement",
    "knee stiffness or tightness",
    "leg swelling",
    "foot or toe swelling",
    "heartburn",
    "infant feeding problem",
    "vaginal pain",
    "vaginal redness",
    "weakness",
    "decreased heart rate",
    "increased heart rate",
    "ringing in ear",
    "plugged feeling in ear",
    "itchy ear(s)",
    "frontal headache",
    "fluid in ear",
    "spots or clouds in vision",
    "eye redness",
    "lacrimation",
    "itchiness of eye",
    "blindness",
    "eye burns or stings",
    "decreased appetite",
    "excessive anger",
    "loss of sensation",
    "focal weakness",
    "symptoms of the face",
    "disturbance of memory",
    "paresthesia",
    "side pain",
    "fever",
    "shoulder pain",
    "shoulder stiffness or tightness",
    "ache all over",
    "lower body pain",
    "problems during pregnancy",
    "spotting or bleeding during pregnancy",
    "cramps and spasms",
    "upper abdominal pain",
    "stomach bloating",
    "changes in stool appearance",
    "unusual color or odor to urine",
    "kidney mass",
    "symptoms of prostate",
    "difficulty breathing",
    "rib pain",
    "joint pain",
    "hand or finger lump or mass",
    "chills",
    "groin pain",
    "fatigue",
    "symptoms of the kidneys",
    "melena",
    "coughing up sputum",
    "seizures",
    "delusions or hallucinations",
    "excessive urination at night",
    "bleeding from eye",
    "rectal bleeding",
    "constipation",
    "temper problems",
    "coryza",
    "hemoptysis",
    "allergic reaction",
    "congestion in chest",
    "sleepiness",
    "apnea",
    "abnormal breathing sounds",
    "blood clots during menstrual periods",
    "pulling at ears",
    "gum pain",
    "redness in ear",
    "fluid retention",
    "flu-like syndrome",
    "sinus congestion",
    "painful sinuses",
    "fears and phobias",
    "recent pregnancy",
    "uterine contractions",
    "burning chest pain",
    "back cramps or spasms",
    "back mass or lump",
    "nosebleed",
    "long menstrual periods",
    "heavy menstrual flow",
    "unpredictable menstruation",
    "painful menstruation",
    "infertility",
    "frequent menstruation",
    "sweating",
    "mass on eyelid",
    "swollen eye",
    "eyelid swelling",
    "eyelid lesion or rash",
    "symptoms of bladder",
    "irregular appearing nails",
    "itching of skin",
    "hurts to breath",
    "skin dryness, peeling, scaliness, or roughness",
    "skin irritation",
    "itchy scalp",
    "warts",
    "skin rash",
    "mass or swelling around the anus",
    "ankle swelling",
    "elbow swelling",
    "bleeding from ear",
    "hand or finger weakness",
    "low self-esteem",
    "itching of the anus",
    "swollen or red tonsils",
    "hip stiffness or tightness",
    "mouth pain",
    "arm weakness",
    "obsessions and compulsions",
    "antisocial behavior",
    "sneezing",
    "leg weakness",
    "hysterical behavior",
    "arm lump or mass",
    "bleeding gums",
    "pain in gums",
    "diaper rash",
    "hesitancy",
    "back stiffness or tightness",
    "low urine output",
]


# =========================================================
# NATURAL LANGUAGE ALIASES
# =========================================================

SYMPTOM_ALIASES = {

    "fever": [
        "fever",
        "high fever",
        "high temperature",
        "temperature",
        "running a fever",
    ],

    "headache": [
        "headache",
        "head pain",
        "pain in my head",
        "pain in head",
        "my head hurts",
        "head hurts",
    ],

    "cough": [
        "cough",
        "coughing",
        "i am coughing",
        "i have a cough",
    ],

    "coughing up sputum": [
        "coughing up sputum",
        "coughing mucus",
        "coughing up mucus",
        "bringing up mucus",
        "phlegm",
        "cough with phlegm",
    ],

    "shortness of breath": [
        "shortness of breath",
        "breathlessness",
        "out of breath",
        "breathing problem",
        "breathing problems",
        "difficulty breathing",
        "hard to breathe",
        "trouble breathing",
    ],

    "difficulty breathing": [
        "difficulty breathing",
        "breathing difficulty",
        "trouble breathing",
        "hard to breathe",
        "cannot breathe properly",
        "can't breathe properly",
    ],

    "sore throat": [
        "sore throat",
        "throat pain",
        "painful throat",
        "my throat hurts",
    ],

    "nausea": [
        "nausea",
        "nauseous",
        "feeling nauseous",
        "feel nauseous",
        "feeling sick",
    ],

    "vomiting": [
        "vomiting",
        "vomit",
        "throwing up",
        "throw up",
        "threw up",
    ],

    "diarrhea": [
        "diarrhea",
        "loose motion",
        "loose stool",
        "watery stool",
    ],

    "dizziness": [
        "dizziness",
        "dizzy",
        "feeling dizzy",
        "lightheaded",
        "light headed",
    ],

    "fatigue": [
        "fatigue",
        "very tired",
        "tired",
        "tiredness",
        "exhausted",
        "feeling exhausted",
    ],

    "weakness": [
        "weakness",
        "feeling weak",
        "weak",
        "very weak",
    ],

    "body pain": [
        "body pain",
        "body ache",
        "body aches",
        "aching all over",
        "body is aching",
    ],

    "ache all over": [
        "ache all over",
        "aching all over",
        "pain all over",
        "body aches everywhere",
    ],

    "joint pain": [
        "joint pain",
        "pain in joints",
        "painful joints",
        "my joints hurt",
    ],

    "chills": [
        "chills",
        "shivering",
        "feeling cold and shivery",
    ],

    "sneezing": [
        "sneezing",
        "sneeze",
        "sneezes",
    ],

    "nasal congestion": [
        "nasal congestion",
        "blocked nose",
        "stuffy nose",
        "congested nose",
    ],

    "sinus congestion": [
        "sinus congestion",
        "blocked sinuses",
        "congested sinuses",
    ],

    "chest pain": [
        "chest pain",
        "pain in chest",
        "pain in my chest",
    ],

    "sharp chest pain": [
        "sharp chest pain",
        "sharp pain in chest",
        "stabbing chest pain",
    ],

    "burning chest pain": [
        "burning chest pain",
        "burning pain in chest",
        "chest burning",
    ],

    "chest tightness": [
        "chest tightness",
        "tight chest",
        "tightness in chest",
    ],

    "palpitations": [
        "palpitations",
        "heart pounding",
        "heart racing",
        "pounding heart",
    ],

    "irregular heartbeat": [
        "irregular heartbeat",
        "irregular heart beat",
        "uneven heartbeat",
        "heart beats irregularly",
    ],

    "increased heart rate": [
        "increased heart rate",
        "fast heart rate",
        "rapid heartbeat",
        "fast heartbeat",
    ],

    "decreased heart rate": [
        "decreased heart rate",
        "slow heart rate",
        "slow heartbeat",
    ],

    "wheezing": [
        "wheezing",
        "wheeze",
    ],

    "back pain": [
        "back pain",
        "pain in my back",
        "my back hurts",
    ],

    "low back pain": [
        "low back pain",
        "lower back pain",
        "pain in lower back",
    ],

    "neck pain": [
        "neck pain",
        "pain in neck",
        "my neck hurts",
    ],

    "shoulder pain": [
        "shoulder pain",
        "pain in shoulder",
        "my shoulder hurts",
    ],

    "knee pain": [
        "knee pain",
        "pain in knee",
        "my knee hurts",
    ],

    "leg pain": [
        "leg pain",
        "pain in leg",
        "my leg hurts",
    ],

    "foot or toe pain": [
        "foot pain",
        "toe pain",
        "pain in foot",
        "pain in toe",
    ],

    "ankle pain": [
        "ankle pain",
        "pain in ankle",
        "my ankle hurts",
    ],

    "arm pain": [
        "arm pain",
        "pain in arm",
        "my arm hurts",
    ],

    "wrist pain": [
        "wrist pain",
        "pain in wrist",
        "my wrist hurts",
    ],

    "elbow pain": [
        "elbow pain",
        "pain in elbow",
        "my elbow hurts",
    ],

    "heartburn": [
        "heartburn",
        "burning in chest after eating",
        "acid reflux",
        "acid burning",
    ],

    "burning abdominal pain": [
        "burning abdominal pain",
        "burning stomach pain",
        "burning pain in stomach",
    ],

    "sharp abdominal pain": [
        "sharp abdominal pain",
        "sharp stomach pain",
        "sharp pain in abdomen",
    ],

    "upper abdominal pain": [
        "upper abdominal pain",
        "upper stomach pain",
        "pain in upper abdomen",
    ],

    "lower abdominal pain": [
        "lower abdominal pain",
        "lower stomach pain",
        "pain in lower abdomen",
    ],

    "stomach bloating": [
        "stomach bloating",
        "bloated stomach",
        "bloating",
        "stomach feels bloated",
    ],

    "constipation": [
        "constipation",
        "constipated",
        "difficulty passing stool",
    ],

    "blood in stool": [
        "blood in stool",
        "blood in my stool",
        "bloody stool",
    ],

    "rectal bleeding": [
        "rectal bleeding",
        "bleeding from rectum",
        "blood from rectum",
    ],

    "painful urination": [
        "painful urination",
        "pain when urinating",
        "burning while urinating",
        "burning urination",
        "pain while peeing",
    ],

    "frequent urination": [
        "frequent urination",
        "urinating frequently",
        "pee frequently",
        "peeing frequently",
    ],

    "low urine output": [
        "low urine output",
        "little urine",
        "very little urine",
        "not producing much urine",
    ],

    "blood in urine": [
        "blood in urine",
        "blood while urinating",
        "bloody urine",
    ],

    "itching of skin": [
        "itching of skin",
        "itchy skin",
        "skin itching",
        "my skin itches",
    ],

    "skin rash": [
        "skin rash",
        "rash",
        "skin rashes",
    ],

    "skin irritation": [
        "skin irritation",
        "irritated skin",
    ],

    "acne or pimples": [
        "acne",
        "pimples",
        "pimple",
        "acne and pimples",
    ],

    "lip swelling": [
        "lip swelling",
        "swollen lips",
        "my lips are swollen",
    ],

    "facial pain": [
        "facial pain",
        "face pain",
        "pain in face",
    ],

    "mouth ulcer": [
        "mouth ulcer",
        "mouth ulcers",
        "oral ulcer",
        "sores in mouth",
    ],

    "toothache": [
        "toothache",
        "tooth pain",
        "pain in tooth",
    ],

    "mouth pain": [
        "mouth pain",
        "pain in mouth",
    ],

    "mouth dryness": [
        "dry mouth",
        "mouth dryness",
    ],

    "eye redness": [
        "red eyes",
        "red eye",
        "eye redness",
        "eyes are red",
    ],

    "itchiness of eye": [
        "itchy eyes",
        "itchiness of eyes",
        "eyes are itchy",
    ],

    "pain in eye": [
        "eye pain",
        "pain in eye",
        "my eye hurts",
    ],

    "diminished vision": [
        "diminished vision",
        "blurred vision",
        "poor vision",
        "reduced vision",
        "vision is blurry",
    ],

    "double vision": [
        "double vision",
        "seeing double",
    ],

    "blindness": [
        "blindness",
        "cannot see",
        "can't see",
        "loss of sight",
    ],

    "ear pain": [
        "ear pain",
        "pain in ear",
        "my ear hurts",
    ],

    "diminished hearing": [
        "diminished hearing",
        "reduced hearing",
        "hearing loss",
        "can't hear properly",
    ],

    "ringing in ear": [
        "ringing in ear",
        "ringing ears",
        "ears ringing",
        "tinnitus",
    ],

    "nosebleed": [
        "nosebleed",
        "bleeding nose",
        "blood from nose",
    ],

    "sweating": [
        "sweating",
        "excessive sweating",
        "sweat a lot",
    ],

    "weight gain": [
        "weight gain",
        "gaining weight",
        "gained weight",
    ],

    "decreased appetite": [
        "decreased appetite",
        "loss of appetite",
        "poor appetite",
        "not hungry",
    ],

    "fainting": [
        "fainting",
        "fainted",
        "passing out",
        "passed out",
    ],

    "insomnia": [
        "insomnia",
        "can't sleep",
        "cannot sleep",
        "difficulty sleeping",
        "trouble sleeping",
    ],

    "restlessness": [
        "restlessness",
        "restless",
        "feeling restless",
    ],

    "sleepiness": [
        "sleepiness",
        "sleepy",
        "very sleepy",
    ],

    "seizures": [
        "seizures",
        "seizure",
        "convulsions",
    ],

    "jaundice": [
        "jaundice",
        "yellow skin",
        "yellow eyes",
    ],

    "diarrhea": [
        "diarrhea",
        "loose stool",
        "loose motion",
    ],

    "allergic reaction": [
        "allergic reaction",
        "allergy",
        "allergic",
    ],

    "feeling ill": [
        "feeling ill",
        "feel ill",
        "feeling sick",
        "feel sick",
        "unwell",
    ],
}


# =========================================================
# NORMALIZE TEXT
# =========================================================

def normalize_text(text: str) -> str:

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# PREPARE LEMMAS
# =========================================================

def get_lemmas(text: str):

    doc = nlp(text)

    return [
        token.lemma_.lower()
        for token in doc
        if not token.is_punct
    ]


# =========================================================
# EXTRACT SYMPTOMS
# =========================================================

def extract_symptoms(text: str):

    normalized_text = normalize_text(text)

    if not normalized_text:
        return []

    detected_symptoms = []

    # -----------------------------------------------------
    # First: exact alias matching
    # -----------------------------------------------------

    for symptom, aliases in SYMPTOM_ALIASES.items():

        if symptom not in SYMPTOMS:
            continue

        for alias in aliases:

            alias_normalized = normalize_text(alias)

            if alias_normalized in normalized_text:

                if symptom not in detected_symptoms:
                    detected_symptoms.append(symptom)

                break

    # -----------------------------------------------------
    # Second: lemma-based matching
    # -----------------------------------------------------

    text_lemmas = get_lemmas(normalized_text)

    for symptom in SYMPTOMS:

        if symptom in detected_symptoms:
            continue

        symptom_lemmas = get_lemmas(symptom)

        if not symptom_lemmas:
            continue

        if all(
            lemma in text_lemmas
            for lemma in symptom_lemmas
        ):
            detected_symptoms.append(symptom)

    return detected_symptoms


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    test_text = """
    I have a high fever, severe headache,
    I am coughing and feeling dizzy.
    My joints hurt and I feel very tired.
    """

    symptoms = extract_symptoms(test_text)

    print("\nDetected symptoms:\n")

    for symptom in symptoms:
        print("✓", symptom)

    print("\nTotal:", len(symptoms))