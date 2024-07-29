from rest_framework import viewsets
from rest_framework.views import APIView

from .models import Student, Teacher, Staff, Course, Attendance, Grade, Activity
from .serializers import StudentSerializer, TeacherSerializer, StaffSerializer, CourseSerializer, AttendanceSerializer, \
    GradeSerializer, ActivitySerializer, RegistrationSerializer, LoginSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentSerializer
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .forms import RegistrationForm
# authentication_classes = [SessionAuthentication, BasicAuthentication]
authentication_classes = [TokenAuthentication]
permission_classes = [IsAuthenticated]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer



@api_view(['POST'])
def register_user(request):
   if request.method == 'POST':
       serializer = StudentSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def user_login(request):
   if request.method == 'POST':
       username = request.data.get('username')
       password = request.data.get('password')


       user = None
       if '@' in username:
           try:
               user = Student.objects.get(email=username)
           except ObjectDoesNotExist:
               pass


       if not user:
           user = authenticate(username=username, password=password)


       if user:
           token, _ = Token.objects.get_or_create(user=user)
           return Response({'token': token.key}, status=status.HTTP_200_OK)


       return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)




@api_view(['POST'])
def user_logout(request):
   if request.method == 'POST':
       try:
           # Delete the user's token to logout
           request.user.auth_token.delete()
           return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
       except Exception as e:
           return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            # Assign role-specific attributes
            if role == 'admin':
                user.is_staff = True
                user.is_superuser = True
                user.save()
            elif role == 'student':
                Student.objects.create(username=user.email, password=user.password, full_name=user.name, role=1)
            elif role == 'teacher':
                Teacher.objects.create(username=user.email, password=user.password, full_name=user.name, role=1)
            elif role == 'staff':
                Staff.objects.create(username=user.email, password=user.password, full_name=user.name, role=1)
            return redirect('login')  # Adjust the redirect URL as needed
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"message": "User logged out successfully"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Invalid token or user not logged in"}, status=status.HTTP_400_BAD_REQUEST)