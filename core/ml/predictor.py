import os
import joblib


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "saved_models",
    "best_model.pkl"
)


model = joblib.load(MODEL_PATH)


def predict_student(study_hours, attendance, previous_marks):

    input_data = [[
        study_hours,
        attendance,
        previous_marks
    ]]

    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(input_data)[0][1]

    return prediction, probability