import os

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import StudentPredictionSerializer
from .ml.predictor import predict_student
from .models import PredictionHistory


@api_view(["POST"])
def predict_student_api(request):

    # ---------------------------------
    # API KEY AUTHENTICATION
    # ---------------------------------
    api_key = request.headers.get("X-API-KEY")
    expected_key = os.environ.get("ML_API_KEY")

    if not expected_key or api_key != expected_key:
        return Response(
            {
                "success": False,
                "message": "Invalid or missing API key"
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    # ---------------------------------
    # INPUT VALIDATION
    # ---------------------------------
    serializer = StudentPredictionSerializer(
        data=request.data
    )

    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    data = serializer.validated_data

    study_hours = data["study_hours"]
    attendance = data["attendance"]
    previous_marks = data["previous_marks"]

    # ---------------------------------
    # ML PREDICTION
    # ---------------------------------
    prediction, probability = predict_student(
        study_hours,
        attendance,
        previous_marks
    )

    if prediction == 1:
        result = "PASS"
    else:
        result = "FAIL"

    probability_percent = round(
        float(probability) * 100,
        2
    )

    # ---------------------------------
    # SAVE PREDICTION HISTORY
    # ---------------------------------
    history = PredictionHistory.objects.create(
        study_hours=study_hours,
        attendance=attendance,
        previous_marks=previous_marks,
        prediction=result,
        probability=probability_percent
    )

    # ---------------------------------
    # API RESPONSE
    # ---------------------------------
    return Response(
        {
            "success": True,
            "message": "Prediction completed successfully",
            "data": {
                "id": history.id,
                "prediction": result,
                "pass_probability": probability_percent
            }
        },
        status=status.HTTP_200_OK
    )