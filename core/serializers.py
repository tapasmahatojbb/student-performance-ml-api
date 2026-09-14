from rest_framework import serializers


class StudentPredictionSerializer(serializers.Serializer):

    study_hours = serializers.FloatField(
        min_value=0,
        max_value=24
    )

    attendance = serializers.FloatField(
        min_value=0,
        max_value=100
    )

    previous_marks = serializers.FloatField(
        min_value=0,
        max_value=100
    )