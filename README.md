# Student Performance Prediction System

An end-to-end Machine Learning web application built with **Python, Scikit-learn, Django, and Django REST Framework**.

The application predicts whether a student is likely to **PASS or FAIL** based on study hours, attendance, and previous marks. It provides prediction probability, stores prediction history, exposes a secured REST API, and includes a responsive web dashboard.

## Live Demo

**Web Application**

https://student-performance-ml-api.onrender.com/

**Prediction API**

```text
POST https://student-performance-ml-api.onrender.com/api/v2/predict/
```

> The application is hosted on Render's free service, so the first request after inactivity may take additional time while the service starts.

---

## Features

- Student PASS / FAIL prediction
- PASS probability calculation
- Professional responsive web interface
- Student CRUD management
- Student search and pagination
- Prediction history
- Prediction analytics dashboard
- Logistic Regression classification
- StandardScaler preprocessing
- Scikit-learn Pipeline
- Hyperparameter tuning using GridSearchCV
- Cross-validation
- Hold-out model evaluation
- Model persistence using Joblib
- Django web integration
- REST API using Django REST Framework
- Environment-based API key protection
- DRF serializer input validation
- Production deployment on Render

---

## Machine Learning Workflow

```text
Student Dataset
      ↓
Feature / Target Separation
      ↓
Train / Test Split
      ↓
Scikit-learn Pipeline
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
Final Model Training
      ↓
Joblib Model Persistence
      ↓
Django Prediction Service
      ↓
Web UI / REST API
```

The preprocessing and Logistic Regression model are stored inside a single Scikit-learn Pipeline. This allows the same preprocessing steps to be applied consistently during both training and prediction.

---

## Model Selection

Multiple classification algorithms were explored during development:

- Decision Tree
- Logistic Regression
- Random Forest

Logistic Regression was selected for the final implementation based on cross-validation results on the project dataset.

The final Logistic Regression pipeline was tuned using `GridSearchCV`.

### Final Model Configuration

```text
Algorithm: Logistic Regression
Preprocessing: StandardScaler
Best C: 0.1
Classification: Binary (PASS / FAIL)
```

---

## Model Evaluation

Final experiment results:

| Metric | Result |
|---|---:|
| Training Cross-Validation Accuracy | 95% |
| Hold-out Accuracy | 100% |
| Precision | 100% |
| Recall | 100% |
| F1 Score | 100% |
| Hold-out Samples | 9 |

### Important Evaluation Note

This project currently uses a small learning/portfolio dataset containing only 30 samples, with 9 samples in the final hold-out test set.

Therefore, the 100% hold-out result **must not be interpreted as 100% expected real-world accuracy**.

A production system would require substantially more representative data, external validation, ongoing performance monitoring, and testing for data drift and generalization.

---

## Technology Stack

### Machine Learning

- Python
- Pandas
- Scikit-learn
- Logistic Regression
- StandardScaler
- GridSearchCV
- Joblib

### Backend

- Django
- Django REST Framework
- DRF Serializers
- SQL Database

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- Bootstrap Icons
- Django Templates

### Deployment

- Git
- GitHub
- Gunicorn
- WhiteNoise
- Render

---

## REST API

### Prediction Endpoint

```http
POST /api/v2/predict/
```

### Authentication

The deployed prediction API is protected using an API key stored securely as an environment variable.

Send the key using:

```http
X-API-KEY: <YOUR_API_KEY>
```

The real API key is **not stored in the source code or GitHub repository**.

### Request

```json
{
    "study_hours": 7,
    "attendance": 80,
    "previous_marks": 70
}
```

### Successful Response

```json
{
    "success": true,
    "message": "Prediction completed successfully",
    "data": {
        "id": 1,
        "prediction": "PASS",
        "pass_probability": 94.03
    }
}
```

The exact probability depends on the trained model.

### Unauthorized Request

A missing or invalid API key returns an authentication error:

```json
{
    "success": false,
    "message": "Invalid or missing API key"
}
```

HTTP status:

```text
401 Unauthorized
```

---

## API Input Validation

The API validates the following feature ranges:

| Feature | Valid Range |
|---|---:|
| Study Hours | 0–24 |
| Attendance | 0–100 |
| Previous Marks | 0–100 |

Invalid input is rejected before reaching the prediction model.

---

## Application Architecture

```text
                  ┌─────────────────────┐
                  │     Web Browser     │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │       Django        │
                  │    Web Interface    │
                  └──────────┬──────────┘
                             │
                             ▼
┌──────────────┐   ┌─────────────────────┐
│ REST Client  │──▶│ Prediction Service  │
└──────────────┘   └──────────┬──────────┘
      │                        │
 X-API-KEY                     ▼
                    ┌─────────────────────┐
                    │ Scikit-learn        │
                    │ Pipeline            │
                    │                     │
                    │ StandardScaler      │
                    │       ↓             │
                    │ Logistic Regression │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ PASS / FAIL         │
                    │ + Probability       │
                    └─────────────────────┘
```

---

## Project Structure

```text
aiweb/
├── aiweb/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/
│   ├── ml/
│   │   ├── students_30.csv
│   │   ├── train_model.py
│   │   ├── predictor.py
│   │   └── saved_models/
│   │       └── best_model.pkl
│   │
│   ├── static/
│   │   └── core/
│   │       └── css/
│   │           └── style.css
│   │
│   ├── templates/
│   │   └── core/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── predict_student.html
│   │       ├── prediction_history.html
│   │       ├── prediction_dashboard.html
│   │       ├── add_student.html
│   │       └── edit_student.html
│   │
│   ├── api_views.py
│   ├── serializers.py
│   ├── models.py
│   └── views.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## Local Installation

Clone the repository:

```bash
git clone https://github.com/tapasmahatojbb/student-performance-ml-api.git
cd student-performance-ml-api
```

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the required environment variables locally.

Train and save the ML model:

```bash
python core/ml/train_model.py
```

Run migrations:

```bash
python manage.py migrate
```

Start Django:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## Security

Sensitive configuration is stored using environment variables rather than hard-coded secrets.

Examples include:

```text
DJANGO_SECRET_KEY
ML_API_KEY
DEBUG
```

Files such as `.env` are excluded from Git version control.

The public repository does not contain the production API key.

---

## Deployment

The application is deployed on Render using:

```text
GitHub
   ↓
Render Build
   ↓
Install Dependencies
   ↓
Train ML Model
   ↓
Django Migrations
   ↓
Collect Static Files
   ↓
Gunicorn
   ↓
Live Application
```

Static assets are served using WhiteNoise.

### Free Deployment Limitation

The current demonstration deployment uses a free hosting configuration. Database-backed prediction history may not be permanently preserved across deployment/restart events when using ephemeral local storage.

For a production deployment, a persistent managed database such as PostgreSQL would normally be used.

---

## Future Improvements

- Collect a larger real-world dataset
- Store verified actual student outcomes
- Separate predicted results from ground-truth labels
- Automated model retraining
- Model versioning
- Model performance monitoring
- Data drift monitoring
- Persistent production database
- Automated tests and CI/CD
- Containerized deployment
- Additional model explainability

---

## Purpose

This project demonstrates an end-to-end Machine Learning development workflow:

**data preparation → model training → evaluation → model persistence → Django integration → REST API → API security → frontend interface → deployment**

It is designed as a practical learning and portfolio project for building production-oriented Python and Machine Learning engineering skills.