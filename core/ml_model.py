from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Student Data
students = [
    [2, 60, 50],
    [3, 65, 55],
    [4, 70, 60],
    [5, 75, 65],
    [6, 80, 70],
    [7, 85, 75],
    [8, 90, 80]
]


# 0 = FAIL
# 1 = PASS
results = [
    0,
    0,
    0,
    1,
    1,
    1,
    1
]


# Training এবং Testing
training_data, test_data, training_result, test_result = train_test_split(
    students,
    results,
    test_size=0.3,
    random_state=10
)


# Model তৈরি
model = DecisionTreeClassifier()


# Model Training
model.fit(training_data, training_result)


# Testing
prediction = model.predict(test_data)


# Accuracy
accuracy = accuracy_score(
    test_result,
    prediction
)


print("Accuracy =", accuracy)


# =========================
# Prediction Function
# =========================

def predict_student(study_hours, attendance, previous_marks):

    student = [[
        study_hours,
        attendance,
        previous_marks
    ]]

    prediction = model.predict(student)

    if prediction[0] == 1:
        return "PASS"
    else:
        return "FAIL"
    

result = predict_student(10, 90, 80)

print("Prediction New Add=", result)