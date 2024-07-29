from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'role']

    def __str__(self):
        return self.email


class Student(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    courses = models.ManyToManyField('Course', related_name='students')
    role = models.IntegerField(choices=[(1, 'Student'), (2, 'Admin')])
    active_user = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


class Teacher(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    teaching_course = models.ManyToManyField('Course', related_name='teachers')
    role = models.IntegerField(choices=[(1, 'Teacher'), (2, 'Admin')])
    active_user = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


class Staff(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    role = models.IntegerField(choices=[(1, 'Staff'), (2, 'Admin')])
    active_user = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


class Course(models.Model):
    course_name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=50, unique=True)
    delivery_mode = models.CharField(max_length=100)

    def __str__(self):
        return self.course_name


class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    attended_students = models.ManyToManyField(Student, related_name='attendances')
    absent_students = models.ManyToManyField(Student, related_name='absences')

    def __str__(self):
        return f'Attendance for {self.course.course_name} on {self.date}'


class Grade(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.CharField(max_length=5)

    def __str__(self):
        return f'{self.student.full_name} - {self.course.course_name} - {self.grade}'


class Activity(models.Model):
    activity_name = models.CharField(max_length=200)
    activity_date = models.DateField()
    students = models.ManyToManyField(Student, related_name='activities')

    def __str__(self):
        return self.activity_name
