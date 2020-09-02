"""loyac_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from loyac_api import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/applicant/', views.ApplicantSignup.as_view(), name="applicant-signup"),
    path('applicant/', views.ApplicantDetails.as_view(), name="applicant-signup"),
    path('signup/staff/', views.StaffSignup.as_view(), name="staff-signup"),
    path('login/', views.MyTokenObtainPairView.as_view(), name="login"),
    path('programs/', views.ProgramList.as_view(), name="programs-list"),
    path('program/create/', views.ProgramCreate.as_view(), name="program-create"),
    path('program/<int:program_id>/', views.ProgramDetails.as_view(), name="program-details"),
    path('applicant/apply/', views.ApplicantProgramApply.as_view(), name="applicant-apply"),
    
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
