from django.shortcuts import render,redirect
from django.http import HttpResponse
from management.email import EmailBackEnd
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages #to show message when entered invalid details or to show any msg like wrong,success,warning etc..
from django.contrib.auth.decorators import login_required
from management.models import CustomUser,Student,Course,Profile
from management.forms import UserRegistrationForm
from management.mail import send_forget_password_email
import uuid


# Create your views here.
def base(request):
    return render(request,'base.html')

def register(request):
    course = Course.objects.all()
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        scholar_number = request.POST.get('scholar_number')
        username = request.POST.get('username')
        password = request.POST.get('password')
        profile_pic = request.FILES.get('profile_pic')
        course = request.POST.get('course')
        branch = request.POST.get('branch')
        course_year = request.POST.get('course_year')
        semester = request.POST.get('semester')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        father_name = request.POST.get('father_name')
        mother_name = request.POST.get('mother_name')
        father_phone_number = request.POST.get('father_phone_number')
        address = request.POST.get('address')
        guardian_name = request.POST.get('guardian_name')
        guardian_phone_number = request.POST.get('guardian_phone_number')
        guardian_address = request.POST.get('guardian_address')
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already taken !')
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already taken !')
            return redirect('add_student')
        else:
            user = CustomUser(first_name=first_name,
                              last_name=last_name,
                              username=username,
                              email=email,
                              profile_pic=profile_pic,
                              userType='2')
            user.set_password(password)  # We just see password option,not the password,it will be encoded.
            user.save()
            course = Course.objects.get(id=course)
            student_obj = Student(
                student=user,
                address=address,
                gender=gender,
                course=course,
                scholar_number=scholar_number,
                student_name=first_name + " " + last_name,
                dob=dob,
                branch=branch,
                father_name=father_name,
                mother_name=mother_name,
                phone_number=phone_number,
                father_phone_number=father_phone_number,
                semester=semester,
                course_year=course_year,
                guardian_name=guardian_name,
                guardian_address=guardian_address,
                guardian_phone_number=guardian_phone_number
            )
            student_obj.save()
            messages.success(request, user.first_name + " " + user.last_name + " is added successfully")
            print('added successfully')
            return redirect('Login')
    context = {
        'course': course,
    }
    return render(request, 'administration/register.html', context)

def Login(request):
    return render(request,'login.html')

def doLogin(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request,username = request.POST.get("email"),
                                    password = request.POST.get("password"))
        if user!=None:
            login(request,user)
            userType = user.userType
            if userType == '1':
                return redirect('administrationHome') #parameter is name in path of URL.
            elif userType == '2':
                return redirect('studentHome')
            elif userType == '3':
                return redirect('wardenHome')
            else:
                messages.error(request,'Entered details are invalid,please enter valid details!!')
                return redirect('Login') #if info is wrong,go back to login page.
        else:
            messages.error(request, 'Entered details are invalid,please enter valid details!!')
            return redirect('Login') #the name parameter of path of url is given to redirect.

def doLogout(request):
    logout(request)
    return redirect('Login')

@login_required(login_url='/')
def profile(request):   #context(dictionary) is used so that we can add model object to our html template
    user = CustomUser.objects.get(id = request.user.id)
    context={
        "user":user,
    }
    return render(request,'profile.html',context) #Parameter is URL as in URL file

@login_required(login_url='/')
def updateProfile(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        #email = request.POST.get('email') #They will be automatically generated
        #username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            customUser = CustomUser.objects.get(id = request.user.id)
            #updating profile using this id.we are storing these values by using id and values got by POST.get method.
            customUser.first_name = first_name
            customUser.last_name = last_name
            if password != None and password != "":
                customUser.set_password(password)
            if profile_pic != None and profile_pic != "":
                customUser.profile_pic = profile_pic
            customUser.save()
            messages.success(request,'Profile updated successfully !')
            return redirect('profile')  #we have to return profile page ,if not return it will be in update_profile page only
        except:
            messages.error(request,'profile isn\'t updated!')
    return render(request, 'profile.html')


def invalid(request):
    return render(request, 'administration/invalid.html')

def change_password(request,token):
    context={}
    try:
       profile = Profile.objects.filter(forget_password_token = token).first()
       context = {'id': profile.user.id,'token':token}
       if request.method == 'POST':
           new_password = request.POST.get('new_password')
           confirm_password = request.POST.get('confirm_password')
           id = request.POST.get('id')
           if id is None:
               messages.success(request,'No user found')
               return redirect(f'/password/change/{token}')
           if new_password != confirm_password:
               messages.success(request, 'New password and confirm password aren\'t same')
               return redirect(f'/password/change/{token}')
           user_obj = CustomUser.objects.get(id = id)
           user_obj.set_password(new_password)
           user_obj.save()
           profile.delete()
           return redirect('Login')


    except Exception as e:
        print(e)
    return render(request,'administration/change_password.html',context)

def forget_password(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            if not CustomUser.objects.filter(email = email).first():
                messages.success(request,'No user found with this username')
                return redirect('forget_password')

            user_obj =  CustomUser.objects.get(email = email)
            print(user_obj)
            token = str(uuid.uuid4())
            try:
                if Profile.objects.get(user=user_obj):
                    return render(request, 'administration/already_mail_sent.html')
            except:
                profile = Profile(user=user_obj, forget_password_token=token)
                profile.save()
                print(profile)
                send_forget_password_email(user_obj.email, token)
                messages.success(request, 'An email is sent.')
                return redirect('forget_password')
    except Exception as e:
        print(e)
    return render(request,'administration/forget_password.html')