from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator,MaxValueValidator
from django.conf import settings
# Create your models here.
#Models means tables in our database
#we have to register models in admin.py to get stored in our database.
class CustomUser(AbstractUser):
    user = (('1','Administration'),('2','Student'),('3','Warden'))
    userType = models.CharField(choices=user,max_length=60,default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic')
    #we have to run
    #py manage.py makemigrations
    #py manage.py migrate
    #to make any changes to custom user.

class Course(models.Model): #here we create model for course and save all options and we get required from dropdown list.
    name = models.CharField(max_length = 100,null = True)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now=True,null = True)
    def __str__(self): #we want name in our database
        return self.name

class year(models.Model):
    year_start = models.CharField(max_length=100,null = True)
    year_end = models.CharField(max_length=100,null = True)
    def __str__(self):
        return self.year_start+" to "+self.year_end


class Room(models.Model):
    room_choice = [('S','Single'),('D','Double'),('T','Triple')]
    room_number = models.CharField(max_length = 100,default=None, unique=True)
    room_type = models.CharField(choices = room_choice,max_length=1,default=None)
    vacant = models.BooleanField(default = False)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(4)])
    present = models.PositiveIntegerField(validators=[MaxValueValidator(4)],default=0,blank=True,null=True)
    def __str__(self):
        return self.room_number

#id field is automatically created by django for every model so no need to mention.
#student details are stored in 2 models student and CustomUser
#if we delete CustomUser,student will be deleted automatically.
#OneToOne --> student optionally can be custom user.
class Student(models.Model):
    student = models.OneToOneField(CustomUser,on_delete = models.CASCADE)
    address = models.TextField()
    gender = models.CharField(max_length=10,null=True)
    course = models.ForeignKey(Course,on_delete=models.DO_NOTHING)
    scholar_number = models.CharField(max_length=15,null=True)
    student_name = models.CharField(max_length=100,null=True)
    dob = models.CharField(max_length=15,null=True)
    branch = models.CharField(max_length=150,null=True)
    father_name = models.CharField(max_length = 100,null=True)
    mother_name = models.CharField(max_length = 100,null=True)
    phone_number = models.CharField(max_length = 10,null=True)
    semester = models.CharField(max_length=5,null=True)
    course_year = models.CharField(max_length=10,null=True)
    room = models.ForeignKey(Room,on_delete=models.DO_NOTHING,blank= True,null = True,unique=False)
    father_phone_number = models.CharField(max_length=100,null=True)
    guardian_name = models.CharField(max_length=100,null=True)
    guardian_phone_number = models.CharField(max_length=100,null=True)
    guardian_address = models.CharField(max_length=100,null=True)
    room_alloted = models.BooleanField(default=False)
    fee_paid = models.BooleanField(default=False)
    def __str__(self):
        return self.scholar_number

class Warden(models.Model):
    warden = models.OneToOneField(CustomUser,default=None,null=True,on_delete= models.CASCADE)
    warden_name = models.CharField(max_length = 100,null=True)
    wardenId = models.CharField(max_length=100,null=True)
    dob = models.CharField(max_length=100,null= True)
    phone_number = models.CharField(max_length=100,null=True)
    dependent_name = models.CharField(max_length=100,null=True)
    dependent_phone_number = models.CharField(max_length=100,null=True)
    address = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.warden_name

class RoomChange(models.Model):
    old_room = models.ForeignKey(Room,on_delete=models.DO_NOTHING,blank=True,null=True,unique=False,related_name='old')
    new_room = models.ForeignKey(Room,on_delete=models.DO_NOTHING,blank=True,null=True,unique=False,related_name='new')
    requester = models.ForeignKey(Student,on_delete = models.DO_NOTHING,blank=True,null=True,unique=False)
    is_approved = models.BooleanField(default=False)
    def __str__(self):
        return self.requester.user.username

class Fee(models.Model):
    student = models.ForeignKey(Student,on_delete = models.DO_NOTHING,blank=True,null=True,unique=False)
    date_paid = models.DateField(auto_now=True)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(10000),MaxValueValidator(30000)])
    is_approved = models.BooleanField(default=False) #is_approved

class NewRegistration(models.Model):
    requester = models.ForeignKey(Student, on_delete=models.DO_NOTHING, blank=True, null=True, unique=False)
    new_room = models.ForeignKey(Room, on_delete=models.DO_NOTHING, blank=True, null=True, unique=False,
                                 related_name='newroom')

class FeeRegister(models.Model):
    fee = models.ForeignKey(Fee,on_delete = models.DO_NOTHING,blank=True,null=True,unique=False)
    receipt = models.FileField(upload_to='media/fee_receipts')

class StudentLeave(models.Model):
    student = models.ForeignKey(Student,on_delete = models.CASCADE,blank = True,null = True,unique = False)
    ticket = models.FileField(upload_to='media/student_leave')
    from_date = models.CharField(max_length = 100,null=True)
    to_date = models.CharField(max_length = 100,null=True)
    message = models.TextField()
    status = models.IntegerField(default=0)
    def __int__(self):
        return self.id

class Complaint(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE,blank = True,null=True,unique=False)
    message = models.TextField()
    reply = models.TextField(null=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.student.student_name

class Checkout(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True, unique=False)
    date = models.CharField(max_length = 100,null=True)
    is_accepted = models.IntegerField(default=0)
    def __str__(self):
        return self.student.student_name

class Expenses(models.Model):
    warden = models.ForeignKey(Warden,on_delete=models.DO_NOTHING,blank=True,null=True,unique=False)
    date = models.DateField(auto_now= True)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(10000),MaxValueValidator(30000)])
    type = models.CharField(max_length=200)
    receipt = models.FileField(upload_to='media/expenses',null=True)
    def __str__(self):
        return self.warden.warden_name


class DateToDateReport(models.Model):
    from_date = models.CharField(max_length=100, null=True)
    to_date = models.CharField(max_length=100, null=True)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(10000), MaxValueValidator(30000)])
    expense = models.ForeignKey(Expenses,on_delete=models.DO_NOTHING,blank=True,null=True,unique=False)
    fee = models.ForeignKey(Fee,on_delete=models.DO_NOTHING,blank=True,null=True,unique=False)

class Administration(models.Model):
    admin = models.OneToOneField(CustomUser,default=None,null=True,on_delete= models.CASCADE)
    admin_name = models.CharField(max_length = 100,null=True)
    adminId = models.CharField(max_length=100,null=True)
    dob = models.CharField(max_length=100,null= True)
    phone_number = models.CharField(max_length=100,null=True)
    dependent_name = models.CharField(max_length=100,null=True)
    dependent_phone_number = models.CharField(max_length=100,null=True)
    address = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.admin_name

class Profile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.user.username





