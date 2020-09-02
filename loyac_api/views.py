from django.shortcuts import render
from .serializers import ApplicantApplySerializer, ApplicantCreateSerializer, StaffCreateSerializer,ProgramListSerializer, ProgramSerializer, ApplicantDetailsSerializer, MyTokenObtainPairSerializer
from .models import Program, Applicant
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView,UpdateAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_list_or_404, get_object_or_404


class ApplicantSignup(CreateAPIView):
    serializer_class = ApplicantCreateSerializer

class StaffSignup(CreateAPIView):
    serializer_class = StaffCreateSerializer

class ProgramList(ListAPIView):
    serializer_class = ProgramListSerializer
    queryset = Program.objects.all()

class ProgramCreate(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):   

      program_serializer = ProgramSerializer(data=request.data)

      if program_serializer.is_valid():
          program_serializer.save()
          return Response(program_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(program_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProgramDetails(RetrieveAPIView):
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'program_id'

class ApplicantDetails(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ApplicantDetailsSerializer
    
    def get_object(self):
        return Applicant.objects.get(user=self.request.user)

class ApplicantProgramApply(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ApplicantApplySerializer

    def get_object(self):
        obj = get_object_or_404(Applicant, user=self.request.user)
        return obj

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer