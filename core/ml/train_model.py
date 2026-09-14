import os
import pandas as pd
import joblib

from sklearn.model_selection import cross_val_score

from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import GridSearchCV


# =========================
# 1. CSV PATH
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(
    BASE_DIR,
    "students_30.csv"
)


# =========================
# 2. LOAD DATA
# =========================

data = pd.read_csv(csv_path)


# =========================
# 3. FEATURES + TARGET
# =========================

features = data[
    [
        "study_hours",
        "attendance",
        "previous_marks"
    ]
]

target = data["result"]


# =========================
# 4. CREATE MODELS
# =========================

decision_tree = DecisionTreeClassifier(
    max_depth=3,
    random_state=42
)


logistic_regression = LogisticRegression(
    max_iter=1000
)


random_forest = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# =========================
# 5. STORE MODELS
# =========================

# models = {
#     "Decision Tree": decision_tree,
#     "Logistic Regression": logistic_regression,
#     "Random Forest": random_forest
# }


models = {
    "Decision Tree": DecisionTreeClassifier(
        max_depth=3,
        random_state=42
    ),

    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000))
    ]),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )
}


# =========================
# 6. CROSS VALIDATION
# =========================

best_model_name = None
best_score = 0


for model_name, model in models.items():

    scores = cross_val_score(
        model,
        features,
        target,
        cv=5,
        scoring="accuracy"
    )

    average_score = scores.mean()

    # print("\n----------------------------")
    # print(model_name)
    # print("----------------------------")

    # print("CV Scores:", scores)

    # print(
    #     "Average Accuracy:",
    #     round(average_score * 100, 2),
    #     "%"
    # )

    if average_score > best_score:

        best_score = average_score
        best_model_name = model_name


# =========================
# 7. BEST MODEL
# =========================

# print("\n============================")
# print("BEST MODEL")
# print("============================")

# print("Model:", best_model_name)

# print(
#     "CV Accuracy:",
#     round(best_score * 100, 2),
#     "%"
# )
        

# =========================
# 8. TRAIN BEST MODEL
# =========================

best_model = models[best_model_name]

best_model.fit(features, target)


# Logistic Regression Pipeline
logistic_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000))
])


# কোন কোন C value পরীক্ষা করব
param_grid = {
    "model__C": [0.01, 0.1, 1, 10, 100]
}


# =========================
# 9. SAVE BEST MODEL
# =========================

# model_path = os.path.join(
#     BASE_DIR,
#     "saved_models",
#     "best_model.pkl"
# )

# joblib.dump(
#     best_model,
#     model_path
# )


# print("\n============================")
# print("MODEL SAVED")
# print("============================")
# print("Path:", model_path)

# grid_search = GridSearchCV(
#     estimator=logistic_pipeline,
#     param_grid=param_grid,
#     cv=5,
#     scoring="accuracy"
# )


# grid_search.fit(features, target)

# print("============================")
# print("LOGISTIC REGRESSION TUNING")
# print("============================")
# print("Best C:", grid_search.best_params_)
# print(
#     "Best CV Accuracy:",
#     round(grid_search.best_score_ * 100, 2),
#     "%"
# )

# # Best tuned pipeline
# best_model = grid_search.best_estimator_

# # Save final tuned model
# model_path = os.path.join(
#     BASE_DIR,
#     "saved_models",
#     "best_model.pkl"
# )

# joblib.dump(best_model, model_path)

# print("============================")
# print("FINAL TUNED MODEL SAVED")
# print("============================")
# print("Path:", model_path)




from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# ---------------------------------
# 1. FINAL HOLD-OUT SPLIT FIRST
# ---------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    features,
    target,
    test_size=0.3,
    random_state=42,
    stratify=target
)


# ---------------------------------
# 2. PIPELINE
# ---------------------------------

logistic_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000))
])


# ---------------------------------
# 3. HYPERPARAMETER SEARCH
#    ONLY ON TRAINING DATA
# ---------------------------------

param_grid = {
    "model__C": [0.01, 0.1, 1, 10, 100]
}

grid_search = GridSearchCV(
    estimator=logistic_pipeline,
    param_grid=param_grid,
    cv=5,
    scoring="accuracy"
)

grid_search.fit(X_train, y_train)


print("============================")
print("LOGISTIC REGRESSION TUNING")
print("============================")

print("Best C:", grid_search.best_params_)

print(
    "Best Training CV Accuracy:",
    round(grid_search.best_score_ * 100, 2),
    "%"
)


# ---------------------------------
# 4. BEST MODEL
# ---------------------------------

best_model = grid_search.best_estimator_


# ---------------------------------
# 5. FINAL TEST
# ---------------------------------

y_pred = best_model.predict(X_test)

print("============================")
print("FINAL HOLD-OUT EVALUATION")
print("============================")

print(
    "Accuracy:",
    round(accuracy_score(y_test, y_pred) * 100, 2),
    "%"
)

print(
    "Precision:",
    round(precision_score(y_test, y_pred) * 100, 2),
    "%"
)

print(
    "Recall:",
    round(recall_score(y_test, y_pred) * 100, 2),
    "%"
)

print(
    "F1 Score:",
    round(f1_score(y_test, y_pred) * 100, 2),
    "%"
)

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("Classification Report:")
print(classification_report(y_test, y_pred))


# ==========================================
# FINAL PRODUCTION MODEL
# ==========================================

best_model = grid_search.best_estimator_

# Train selected model using all available data
best_model.fit(features, target)

model_path = os.path.join(
    BASE_DIR,
    "saved_models",
    "best_model.pkl"
)

joblib.dump(best_model, model_path)

print("============================")
print("FINAL PRODUCTION MODEL SAVED")
print("============================")
print("Best C:", grid_search.best_params_)
print("Path:", model_path)