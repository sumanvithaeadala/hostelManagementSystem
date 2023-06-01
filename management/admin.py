from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class UserModel(UserAdmin):
    list_display =['username','userType']
admin.site.register(CustomUser,UserModel)
admin.site.register(Course)
admin.site.register(year)
admin.site.register(Fee)
admin.site.register(Room)
admin.site.register(Student)
admin.site.register(Warden)
admin.site.register(RoomChange)
admin.site.register(NewRegistration)
admin.site.register(FeeRegister)
admin.site.register(StudentLeave)
admin.site.register(Complaint)
admin.site.register(Checkout)