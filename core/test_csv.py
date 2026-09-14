import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score
)

# 1. CSV Load
data = pd.read_csv("core/students_30.csv")


# 2. Features
features = data[
    ["study_hours", "attendance", "previous_marks"]
]


# 3. Target
target = data["result"]


# 4. Train / Test Split
training_data, test_data, training_result, test_result = train_test_split(
    features,
    target,
    test_size=0.3,
    random_state=10,
    stratify=target
)


# 5. Logistic Regression Model
model = LogisticRegression(
    max_iter=1000
)


# 6. Training
model.fit(
    training_data,
    training_result
)


# 7. Prediction
prediction = model.predict(
    test_data
)


# 8. Metrics
accuracy = accuracy_score(test_result, prediction)
precision = precision_score(test_result, prediction)
recall = recall_score(test_result, prediction)
f1 = f1_score(test_result, prediction)
cm = confusion_matrix(test_result, prediction)


# 9. Output
# print("\nACTUAL:")
# print(test_result.values)

# print("\nPREDICTION:")
# print(prediction)

# print("\nLOGISTIC REGRESSION RESULT:")
# print("Accuracy =", round(accuracy * 100, 2), "%")
# print("Precision =", round(precision * 100, 2), "%")
# print("Recall =", round(recall * 100, 2), "%")
# print("F1 Score =", round(f1 * 100, 2), "%")

# print("\nCONFUSION MATRIX:")
# print(cm)

# probability = model.predict_proba(test_data)

# print("\nPROBABILITY:")
# print(probability)

probability = model.predict_proba(test_data)

pass_probability = probability[:, 1]

print("\nPASS PROBABILITY:")

for value in pass_probability:
    print(round(value * 100, 2), "%")