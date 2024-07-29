from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, TeacherViewSet, StaffViewSet, CourseViewSet, AttendanceViewSet, GradeViewSet, \
    ActivityViewSet, RegisterView, LoginView, LogoutView
from .views import register
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'attendances', AttendanceViewSet)
router.register(r'grades', GradeViewSet)
router.register(r'activities', ActivityViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/',  LoginView.as_view(), name='logout'),
]
