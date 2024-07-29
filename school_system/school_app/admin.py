from django.contrib import admin
from .models import Student, Teacher, Staff, Course, Attendance, Grade, Activity, CustomUser

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Staff)
admin.site.register(Course)
admin.site.register(Attendance)
admin.site.register(Grade)
admin.site.register(Activity)
admin.site.register(CustomUser)
