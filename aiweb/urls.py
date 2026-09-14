"""
URL configuration for aiweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from core.views import (
    home,
    add_student,
    edit_student,
    delete_student,
    prediction_page,
    predict_student_view,
    prediction_history,
    prediction_dashboard,
    prediction_api
)

from core.api_views import predict_student_api


urlpatterns = [

    path('admin/', admin.site.urls),

    path('', home),

    path(
        'student/add/',
        add_student
    ),

    path(
        'student/edit/<int:id>',
        edit_student
    ),

    path(
        'student/delete/<int:id>',
        delete_student
    ),

    path(
        'prediction/',
        prediction_page
    ),

    path(
        'predict/',
        predict_student_view,
        name='predict_student'
    ),

    path(
    "prediction-history/",
    prediction_history,
    name="prediction_history"
    ),

    path(
    "prediction-dashboard/",
    prediction_dashboard,
    name="prediction_dashboard"
    ),

    path(
    "api/predict/",
    prediction_api,
    name="prediction_api"
    ),

    path(
    "api/v2/predict/",
    predict_student_api,
    name="predict_student_api"
    ),


    

]