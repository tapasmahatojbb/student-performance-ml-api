from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .ml_model import predict_student
from django.shortcuts import render
from .ml.predictor import predict_student
from .models import PredictionHistory
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt




# Create your views here.


def home(request):
    # name="Tapas"
    # city="Purulia"
    # goal="AI/ML Developer"
    # marks= 75
    search = request.GET.get("search", "")
    marks = request.GET.get("marks", "")

    students = Student.objects.all()

    if search:
        students = Student.objects.filter(
         Q(name__icontains=search) |
         Q(city__icontains=search)   
        )
    if marks:
        students = Student.objects.filter(
            marks__gte=marks
        )
    
    paginator = Paginator(students, 2)

    page_number = request.GET.get("page")

    students = paginator.get_page(page_number)

        

    return render(request,"core/home.html",{
        'students':students,
        "search": search,
        'marks':marks
        
    })

def add_student(request):

    if request.method == "POST":

        #data = request.POST.dict()

        #return HttpResponse(f"<pre>{data}</pre>")

        name = request.POST["name"]
        age = request.POST["age"]
        city = request.POST["city"]
        marks = request.POST["marks"]

        Student.objects.create(
            name=name,
            age=age,
            city=city,
            marks=marks
        )

        messages.success(request, "Student added successfully!")

        return redirect("/")

    return render(request, "core/add_student.html")

def edit_student(request,id):

    student = Student.objects.get(id=id)

    if request.method=='POST':
        student.name = request.POST["name"]
        student.age = request.POST["age"]
        student.city = request.POST["city"]
        student.marks = request.POST["marks"]
        student.save()
        messages.success(request,'Student data Update Successful')
        return redirect('/')
    return render(request, 'core/edit_student.html',{
        'student': student
    }
    )
def delete_student(request,id):
    student = Student.objects.get(id=id)
    student.delete()
    messages.success(request,'Student data Delete Successful')
    return redirect('/')

def prediction_page(request):

    result = None
    error = None

    if request.method == "POST":

        study_hours = int(request.POST["study_hours"])
        attendance = int(request.POST["attendance"])
        previous_marks = int(request.POST["previous_marks"])

        if study_hours < 0 or study_hours > 24:
            error = "Study Hours must be between 0 and 24."

        elif attendance < 0 or attendance > 100:
            error = "Attendance must be between 0 and 100."

        elif previous_marks < 0 or previous_marks > 100:
            error = "Previous Marks must be between 0 and 100."

        else:
            result = predict_student(
                study_hours,
                attendance,
                previous_marks
            )

    return render(request, "core/prediction.html", {
        "result": result,
        "error": error
    })

# def predict_student_view(request):
#     result = None
#     probability_percent = None

#     if request.method == "POST":

#         study_hours = float(request.POST.get("study_hours"))
#         attendance = float(request.POST.get("attendance"))
#         previous_marks = float(request.POST.get("previous_marks"))

#         prediction, probability = predict_student(
#             study_hours,
#             attendance,
#             previous_marks
#         )

#         if prediction == 1:
#             result = "PASS"
#         else:
#             result = "FAIL"

#         probability_percent = round(
#             probability * 100,
#             2
#         )

#     return render(
#         request,
#         "core/predict_student.html",
#         {
#             "result": result,
#             "probability": probability_percent
#         }
#     )

def predict_student_view(request):

    result = None
    probability_percent = None

    if request.method == "POST":

        study_hours = float(
            request.POST.get("study_hours")
        )

        attendance = float(
            request.POST.get("attendance")
        )

        previous_marks = float(
            request.POST.get("previous_marks")
        )

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
            probability * 100,
            2
        )

        # Save prediction in database
        PredictionHistory.objects.create(
            study_hours=study_hours,
            attendance=attendance,
            previous_marks=previous_marks,
            prediction=result,
            probability=probability_percent
        )

    return render(
        request,
        "core/predict_student.html",
        {
            "result": result,
            "probability": probability_percent
        }
    )

def prediction_history(request):

    histories = PredictionHistory.objects.all().order_by("-created_at")

    return render(
        request,
        "core/prediction_history.html",
        {
            "histories": histories
        }
    )

def prediction_dashboard(request):

    total_predictions = PredictionHistory.objects.count()

    total_pass = PredictionHistory.objects.filter(
        prediction="PASS"
    ).count()

    total_fail = PredictionHistory.objects.filter(
        prediction="FAIL"
    ).count()

    if total_predictions > 0:
        pass_rate = round(
            (total_pass / total_predictions) * 100,
            2
        )
    else:
        pass_rate = 0

    return render(
        request,
        "core/prediction_dashboard.html",
        {
            "total_predictions": total_predictions,
            "total_pass": total_pass,
            "total_fail": total_fail,
            "pass_rate": pass_rate
        }
    )


@csrf_exempt
def prediction_api(request):

    # Only POST request allowed
    if request.method != "POST":
        return JsonResponse(
            {
                "error": "Only POST request is allowed"
            },
            status=405
        )

    try:
        # JSON request body read
        data = json.loads(request.body)

        required_fields = [
            "study_hours",
            "attendance",
            "previous_marks"
        ]

        for field in required_fields:
            if field not in data:
                return JsonResponse(
                    {
                        "error": f"{field} is required"
                    },
                    status=400
                )

        # study_hours = float(
        #     data.get("study_hours")
        # )

        # attendance = float(
        #     data.get("attendance")
        # )

        # previous_marks = float(
        #     data.get("previous_marks")
        # )

        # # ML Prediction
        # prediction, probability = predict_student(
        #     study_hours,
        #     attendance,
        #     previous_marks
        # )


        study_hours = float(data.get("study_hours"))
        attendance = float(data.get("attendance"))
        previous_marks = float(data.get("previous_marks"))

        # Validation
        if study_hours < 0 or study_hours > 24:
            return JsonResponse(
                {"error": "Study hours must be between 0 and 24"},
                status=400
            )

        if attendance < 0 or attendance > 100:
            return JsonResponse(
                {"error": "Attendance must be between 0 and 100"},
                status=400
            )

        if previous_marks < 0 or previous_marks > 100:
            return JsonResponse(
                {"error": "Previous marks must be between 0 and 100"},
                status=400
            )

        # Only valid data reaches the ML model
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
            probability * 100,
            2
        )

        # Save API prediction to database
        PredictionHistory.objects.create(
            study_hours=study_hours,
            attendance=attendance,
            previous_marks=previous_marks,
            prediction=result,
            probability=probability_percent
        )

        # JSON response
        return JsonResponse(
            {
                "prediction": result,
                "pass_probability": probability_percent
            },
            status=200
        )

    except (TypeError, ValueError, json.JSONDecodeError):

        return JsonResponse(
            {
                "error": "Invalid input data"
            },
            status=400
        )

    