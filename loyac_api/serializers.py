from rest_framework import serializers
from .models import User, AgeGroup, Program, Applicant
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

#-------------------------------------------------------
class AgeGroupSerializer(serializers.ModelSerializer):
	class Meta:
		model= AgeGroup
		fields = '__all__'


class ProgramSerializer(serializers.ModelSerializer):
	class Meta:
		model = Program
		fields = '__all__'

class ProgramListSerializer(serializers.ModelSerializer):
	age_group=AgeGroupSerializer()
	class Meta:
		model = Program
		fields = '__all__'

class ProgramIDSerializer(serializers.ModelSerializer):
	class Meta:
		model = Program
		fields = ['id', 'age_group']		

class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	is_staff = serializers.BooleanField(default=False, required=False)
	class Meta:
		model=User
		fields=['first_name','last_name','email', 'birth_date', 'password', 'is_staff']

	def create(self, validated_data):
		new_user = User(**validated_data)
		new_user.set_password(validated_data['password'])
		new_user.save()
		return validated_data

class ApplicantCreateSerializer(serializers.ModelSerializer):
	user=UserSerializer()

	class Meta:
		model = Applicant
		fields = ['user']

	def create(self, validated_data):
		user_data = validated_data.pop('user')
		raw_password = user_data.pop('password')
		user_instance = User.objects.create(**user_data)
		user_instance.set_password(raw_password)
		user_instance.save()
		applicant_instance = Applicant.objects.create(user=user_instance, **validated_data)
		return applicant_instance


class ApplicantDetailsSerializer(serializers.ModelSerializer):
	user=UserSerializer()
	program=ProgramIDSerializer(many=True)
	class Meta:
		model = Applicant
		fields = ['user', 'program', 'age', 'total_points']


class ApplicantApplySerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Applicant
		fields = ['program']

		
class StaffCreateSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	is_staff = serializers.BooleanField(default=True, required=False)
	class Meta:
		model = User
		fields = ['first_name','last_name','email','birth_date', 'password', 'is_staff']

	def create(self, validated_data):
		new_user = User(**validated_data)
		new_user.set_password(validated_data['password'])
		new_user.save()
		return validated_data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)
		token['is_staff'] = user.is_staff
		return token