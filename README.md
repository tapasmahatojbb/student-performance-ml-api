# Student Performance Prediction System

An end-to-end Machine Learning web application built with Python, Scikit-learn, Django and Django REST Framework.

The system predicts whether a student is likely to PASS or FAIL based on study hours, attendance and previous marks. It also provides prediction probability and stores prediction history for tracking and analysis.

## Features

- Student PASS/FAIL prediction
- Prediction probability
- Logistic Regression classification
- StandardScaler preprocessing
- Scikit-learn Pipeline
- Hyperparameter tuning using GridSearchCV
- Hold-out model evaluation
- Model persistence using Joblib
- Django web integration
- REST API using Django REST Framework
- Token-based API authentication
- Input validation using DRF Serializers
- Prediction history stored in database
- Prediction dashboard

## Machine Learning Pipeline

```text
Dataset
   ↓
Train/Test Split
   ↓
StandardScaler
   ↓
Logistic Regression
   ↓
GridSearchCV
   ↓
Best Hyperparameters
   ↓
Hold-out Evaluation
   ↓
Final Production Model
   ↓
Joblib Model
   ↓
Django / REST API
```

## Model Evaluation

The selected Logistic Regression model was tuned using GridSearchCV.

- Best C: 0.1
- Training Cross-Validation Accuracy: 95%
- Hold-out Test Accuracy: 100%
- Precision: 100%
- Recall: 100%
- F1 Score: 100%

The hold-out test set contained only 9 samples because this is a small learning/portfolio dataset. Therefore, the test results should not be interpreted as evidence of 100% real-world accuracy.

## Technology Stack

- Python
- Pandas
- Scikit-learn
- Django
- Django REST Framework
- Joblib
- SQL Database
- REST API
- Token Authentication

## API

### Prediction Endpoint

```text
POST /api/v2/predict/
```

Authentication:

```text
Authorization: Token <YOUR_TOKEN>
```

Example request:

```json
{
    "study_hours": 7,
    "attendance": 80,
    "previous_marks": 70
}
```

Example response:

```json
{
    "success": true,
    "message": "Prediction completed successfully",
    "data": {
        "id": 14,
        "prediction": "PASS",
        "pass_probability": 94.03
    }
}
```

## Input Validation

The API validates:

- Study hours: 0–24
- Attendance: 0–100
- Previous marks: 0–100

Invalid requests return HTTP 400 validation errors.

## Project Structure

```text
aiweb/
├── core/
│   ├── ml/
│   │   ├── students_30.csv
│   │   ├── train_model.py
│   │   ├── predictor.py
│   │   └── saved_models/
│   │       └── best_model.pkl
│   ├── api_views.py
│   ├── serializers.py
│   ├── models.py
│   └── views.py
├── aiweb/
├── manage.py
└── README.md
```

## Future Improvements

- Collect larger real-world datasets
- Store verified actual outcomes
- Automated model retraining
- Model versioning
- Model performance monitoring
- Deployment