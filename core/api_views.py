from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes
)

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import StudentPredictionSerializer
from .ml.predictor import predict_student
from .models import PredictionHistory


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def predict_student_api(request):

    serializer = StudentPredictionSerializer(
        data=request.data
    )

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    data = serializer.validated_data

    study_hours = data["study_hours"]
    attendance = data["attendance"]
    previous_marks = data["previous_marks"]

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

    history = PredictionHistory.objects.create(
        study_hours=study_hours,
        attendance=attendance,
        previous_marks=previous_marks,
        prediction=result,
        probability=probability_percent
    )

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