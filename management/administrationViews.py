from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from management.models import Course,year,Student,CustomUser,Room,Warden,NewRegistration,Fee,RoomChange,FeeRegister,StudentLeave,Complaint,Checkout,Expenses,Administration
from django.contrib import messages
from django.http import HttpResponse
from django.db import transaction
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from management.forms import RejectForm,ReportForm
from django.db.models import Sum

@login_required(login_url='/')
def home(request):
    return render(request,'administration/home.html') #the parameter is html file which has to show on screen.

@login_required(login_url='/')
def addStudent(request):
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
            messages.warning(request,'Email is already taken !')
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,'Username is already taken !')
            return redirect('add_student')
        else:
            user = CustomUser(first_name=first_name,
                              last_name = last_name,
                              username= username,
                              email=email,
                              profile_pic = profile_pic,
                              userType='2')
            user.set_password(password) #We just see password option,not the password,it will be encoded.
            user.save()
            course=Course.objects.get(id=course)
            student_obj = Student(
                student = user,
                address = address,
                gender = gender,
                course = course,
                scholar_number=scholar_number,
                student_name = first_name+" "+last_name,
                dob = dob,
                branch = branch,
                father_name = father_name,
                mother_name = mother_name,
                phone_number = phone_number,
                father_phone_number=father_phone_number,
                semester = semester,
                course_year = course_year,
                guardian_name = guardian_name,
                guardian_address = guardian_address,
                guardian_phone_number = guardian_phone_number
            )
            student_obj.save()
            messages.success(request,user.first_name+" "+user.last_name+" is added successfully")
            return redirect('add_student')
    context = {
        'course': course,
    }
    return render(request,'administration/addStudent.html',context)

@login_required(login_url='/')
def studentlist(request):
    student = Student.objects.all()
    context = {
               'student':student,
        }
    return render(request,'administration/studentlist.html',context)

@login_required(login_url='/')
def edit_student(request,id):
    student = Student.objects.filter(id=id)
    course = Course.objects.all()

    context={
        'student':student,
        'course':course,
    }
    return render(request,'administration/editStudent.html',context)

@login_required(login_url='/')
def update_student(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
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
        #If we get id,we update(if there is no id we can't update
        user = CustomUser.objects.get(id = student_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()
        student_obj = Student.objects.get(student = student_id)
        student_obj.student = user
        student_obj.student_name = first_name+" "+last_name
        student_obj.address = address
        student_obj.gender = gender
        course = Course.objects.get(id = course)
        student_obj.course=course
        student_obj.save()
        messages.success(request,'Record updated successfully !')
        return redirect('studentlist')
    return render(request,'administration/editStudent.html')

@login_required(login_url='/')
def delete_student(request,student):
    student_obj = CustomUser.objects.get(id = student)
    student_obj.delete()
    messages.success(request,'Record deleted successfully !')
    return redirect('studentlist')

@login_required(login_url='/')
def student_details(request,id):
    student = Student.objects.filter(id = id)
    context={
        'student':student,
    }

    return render(request,'administration/studentdetails.html',context)

@login_required(login_url='/')
def add_warden(request):
    if request.method=="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        wardenId = request.POST.get('wardenId')
        profile_pic = request.FILES.get('profile_pic')
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        dependent_name = request.POST.get('dependent_name')
        dependent_phone_number = request.POST.get('dependent_phone_number')
        address = request.POST.get('address')
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Email is already taken!')
            return redirect('add_warden')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'username is already taken!')
            return redirect('add_warden')
        else:
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email=email,
                profile_pic = profile_pic,
                userType='3',
            )
            user.set_password(password)
            user.save()
            warden_obj = Warden(
                warden = user,
                address=address,
                warden_name = first_name+" "+last_name,
                dob= dob,
                phone_number = phone_number,
                wardenId= wardenId,
                dependent_name = dependent_name,
                dependent_phone_number = dependent_phone_number,
            )
            warden_obj.save()
            messages.success(request,'Warden added successfully !')
            return redirect('add_warden')
    return render(request,'administration/add_warden.html')

@login_required(login_url='/')
def wardenlist(request):
    warden_obj = Warden.objects.all()
    context={
        'warden_obj':warden_obj,
    }
    return render(request,'administration/wardenlist.html',context)

@login_required(login_url='/')
def edit_warden(request,warden):
    admin_obj = Administration.objects.filter(id=warden)
    context={
       'admin_obj':admin_obj,
    }
    return render(request,'administration/editWarden.html',context)

@login_required(login_url='/')
def update_warden(request):
    if request.method == "POST":
        wardenid = request.POST.get('wardenid')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        wardenId = request.POST.get('wardenId')
        profile_pic = request.FILES.get('profile_pic')
        username = request.POST.get('username')
        password = request.POST.get('password')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        dependent_name = request.POST.get('dependent_name')
        dependent_phone_number = request.POST.get('dependent_phone_number')
        address = request.POST.get('address')
        user = CustomUser.objects.get(id = wardenid)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email=email
        if password != None and password !="":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()
        warden_obj = Warden.objects.get(warden = wardenid)
        warden_obj.warden = user
        warden_obj.wardenId = wardenId
        warden_obj.warden_name = first_name+" "+last_name
        warden_obj.dob =dob
        warden_obj.phone_number = phone_number
        warden_obj.dependent_name = dependent_name
        warden_obj.dependent_phone_number = dependent_phone_number
        warden_obj.address = address
        warden_obj.save()
        messages.success(request,'Record updated successfully')
        return redirect('wardenlist')
    return render(request,'administration/editWarden.html')

@login_required(login_url='/')
def delete_warden(request,id): #id is not warden's ,it is customuser's
    warden_obj = CustomUser.objects.get(id = id)
    warden_obj.delete()
    messages.success(request,'Record deleted successfully !')
    return redirect('wardenlist')

@login_required(login_url='/')
def warden_details(request,id):
    warden_obj = Warden.objects.filter(id = id)
    context={
        'warden_obj':warden_obj,
    }
    return render(request,'administration/wardendetails.html',context)

@login_required(login_url='/')
def add_admin(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        adminId = request.POST.get('adminId')
        profile_pic = request.FILES.get('profile_pic')
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        dependent_name = request.POST.get('dependent_name')
        dependent_phone_number = request.POST.get('dependent_phone_number')
        address = request.POST.get('address')
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already taken!')
            return redirect('add_admin')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'username is already taken!')
            return redirect('add_admin')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                userType='1',
            )
            user.set_password(password)
            user.save()
            admin_obj = Administration(
                admin=user,
                address=address,
                admin_name=first_name + " " + last_name,
                dob=dob,
                phone_number=phone_number,
                adminId=adminId,
                dependent_name=dependent_name,
                dependent_phone_number=dependent_phone_number,
            )
            admin_obj.save()
            messages.success(request, 'Admin added successfully !')
            return redirect('add_admin')
    return render(request, 'administration/addAdmin.html')

@login_required(login_url='/')
def admin_list(request):
    admin_obj = Administration.objects.all()
    context={
        'admin_obj':admin_obj,
    }
    return render(request,'administration/adminList.html',context)

@login_required(login_url='/')
def edit_admin(request,admin):
    admin_obj = Administration.objects.filter(id=admin)
    context={
       'admin_obj':admin_obj,
    }
    return render(request,'administration/editAdmin.html',context)

@login_required(login_url='/')
def update_admin(request):
    if request.method == "POST":
        adminid = request.POST.get('adminid')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        adminId = request.POST.get('adminId')
        profile_pic = request.FILES.get('profile_pic')
        username = request.POST.get('username')
        password = request.POST.get('password')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        dependent_name = request.POST.get('dependent_name')
        dependent_phone_number = request.POST.get('dependent_phone_number')
        address = request.POST.get('address')
        user = CustomUser.objects.get(id = adminid)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email=email
        if password != None and password !="":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()
        admin_obj = Administration.objects.get(admin = adminid)
        admin_obj.admin = user
        admin_obj.adminId = adminId
        admin_obj.admin_name = first_name+" "+last_name
        admin_obj.dob =dob
        admin_obj.phone_number = phone_number
        admin_obj.dependent_name = dependent_name
        admin_obj.dependent_phone_number = dependent_phone_number
        admin_obj.address = address
        admin_obj.save()
        messages.success(request,'Record updated successfully')
        return redirect('admin_list')
    return render(request,'administration/editAdmin.html')

@login_required(login_url='/')
def admin_details(request,id):
    admin_obj = Administration.objects.filter(id = id)
    context={
        'admin_obj':admin_obj,
    }
    return render(request,'administration/admindetails.html',context)


@login_required(login_url='/')
def delete_admin(request,id): #id is not admin's ,it is customuser's
    admin_obj = CustomUser.objects.get(id = id)
    admin_obj.delete()
    messages.success(request,'Record deleted successfully !')
    return redirect('admin_list')

@login_required(login_url='/')
def add_room(request):
    if request.method == "POST":
        room_number = request.POST.get('room_number')
        room_type = request.POST.get('room_type')
        if room_type == 'S':
            capacity = 1
        elif room_type == 'D':
            capacity = 2
        elif room_type == 'T':
            capacity = 3
        print(room_number,room_type,capacity)
        if Room.objects.filter(room_number=room_number).exists():
            messages.warning(request, 'Room already exist!')
            return redirect('add_room')
        else:
            room = Room(
                room_number=room_number,
                room_type=room_type,
                capacity=capacity,
            )
            room.save()
            return redirect('roomlist_aw')
    return render(request,'administration/addRoom.html')

@login_required(login_url='/')
def roomlist(request): #student to select room
    try:
        current_user = request.user
        obj = Student.objects.filter(student=current_user)
        s = NewRegistration.objects.get(requester=obj)
        return render(request, 'administration/room_notallowed.html')
    except:
        rooms = Room.objects.all()
        roomdata = []
        for x in rooms:
            remains = x.capacity - x.present
            type = x.room_type
            if type == 'S':
                amount = 15000
            elif type == 'D':
                amount = 12000
            elif type == 'T':
                amount = 9000
            y = {'room_number': x.room_number, 'room_type': x.room_type, 'present': x.present, 'remains': remains,
                 'fees': amount}
            roomdata.append(y)
        context = {'roomdata': roomdata}
        return render(request, 'administration/roomlist.html', context)

@login_required(login_url='/')
def selectRoom(request,id):
    current_user=request.user
    obj = Student.objects.get(student=current_user)
    if obj.room==None:
        try:
            s = NewRegistration.objects.get(requester__student__username=request.user)
            return render(request, 'administration/room_notallowed.html')
        except:
            current_user = request.user
            obj = Student.objects.get(student=current_user)
            if obj.room == None:
                room = NewRegistration()
                room.requester = obj
                room.new_room = Room.objects.get(room_number=id)
                room.save()
                context = {
                    'room_number': id,
                }
                return render(request, 'administration/roomConfirm.html', context)
    else:
        return render(request, 'administration/only_new.html')


@login_required(login_url='/')
def roomDetails(request,id):
    r = str(id)
    students = Student.objects.select_related('student').select_related('room').filter(room__room_number=r)
    student_data=[]
    print(r)
    for x in students:
        try:
            l={
                'student_name':x.student_name,
                'scholar_number':x.scholar_number,
                 'gender':x.gender,
                'course':x.course,
                'dob':x.dob,
                'branch':x.branch,
                'father_name':x.father_name,
                 'mother_name':x.mother_name,
                  'phone_number':x.phone_number,
                 'semester':x.semester,
                 'course_year':x.course_year,
                 'father_phone_number':x.father_phone_number,
                'guardian_name':x.guardian_name,
                'guardian_phone_number':x.guardian_phone_number,
                'guardian_address':x.guardian_address,
                 'room':x.room.room_number,
                  'fee_paid':x.fee_paid,

            }
            student_data.append(l)
        except:
            print('error')
    context={'student_data':student_data,'room':id}
    return render(request,'administration/roomDetails.html',context)


@login_required(login_url='/')
def roomlist_aw(request):
    room = Room.objects.all()
    room_data = []
    for i in room:
        remains = i.capacity - i.present
        y = {
            'room_number': i.room_number,
            'room_type': i.room_type,
            'present': i.present,
            'remains': remains,
            'capacity':i.capacity,
        }
        room_data.append(y)
        context = {
            'room_data': room_data,
        }
    return render(request,'administration/roomlist_aw.html',context)

@login_required(login_url='/')
def room_change_view(request):
    room = Room.objects.all()
    obj = Student.objects.get(student = request.user)
    room_data = []
    for x in room:
        if x != obj.room:
            remains = x.capacity - x.present
            room_type = x.room_type
            if room_type == 'S':
                amount = 15000
            elif room_type == 'D':
                amount = 12000
            elif room_type == 'T':
                amount = 9000
            y = {
                'room_number': x.room_number,
                'room_type': x.room_type,
                'present': x.present,
                'remains': remains,
                'fees': amount,
            }
            room_data.append(y)
    context ={
        'room_data':room_data,
    }
    return render(request,'administration/change_allrooms.html',context)


@login_required(login_url='/')
def room_change_approval(request,id):
    current_user = request.user
    obj = Student.objects.get(student = current_user)
    if obj.room!=None:
        try:
            s= RoomChange.objects.get(requester__student__username = request.user)
            return render(request,'administration/room_notallowed.html')
        except:
            req = RoomChange()
            req.requester = obj
            req.old_room = obj.room
            robj = Room.objects.get(room_number=id)
            req.new_room = robj
            req.save()
            transaction.commit()
            context = {
                'room': id,
            }
            return render(request, 'administration/request.html', context)
    else:
        return render(request, 'administration/new_canselect.html')

@login_required(login_url='/')
def approve_all_view_warden(request): #warden
    app = RoomChange.objects.all()
    app_data=[]
    for x in app:
        if not x.is_approved:
            y={
                'old_room':x.old_room.room_number,
                'new_room':x.new_room.room_number,
                'requester':x.requester.student_name,
                'course':x.requester.course,
                'course_year':x.requester.course_year,
                'branch':x.requester.branch,
                'username':x.requester.student.username,
            }
            app_data.append(y)
    context={
        'app_data':app_data,
    }
    return render(request,'administration/approveList.html',context)

@login_required(login_url='/')
def new_approve_all_view_warden(request):
    app = NewRegistration.objects.all()
    app_data=[]
    for x in app:
        y={
            'new_room':x.new_room.room_number,
            'requester':x.requester.student_name,
            'course':x.requester.course,
            'username':x.requester.student.username,
            'vacant':x.new_room.capacity - x.new_room.present,
            'present':x.new_room.present,
        }
        app_data.append(y)
    context={
        'app_data':app_data,
    }
    return render(request,'administration/approval_list_new.html',context)

@login_required(login_url='/')
def approve_confirm(request,id):
    app = RoomChange.objects.filter(requester__student__username = id).first()
    student_obj = Student.objects.get(student__username = id)
    old_room = student_obj.room
    new_room = app.new_room
    if new_room.present == new_room.capacity:
        app.delete()
        transaction.commit()
        subject = 'Your request has been cancelled'
        message = 'The room was already full.So,your room change request has been cancelled by the warden '
        email_from = settings.EMAIL_HOST_USER
        recipient_list=[student_obj.student.email]
        send_mail(subject,message,email_from,recipient_list)
        return redirect('approval_list')
    else:
        old_room.present = old_room.present - 1
        new_room.present =  new_room.present + 1
        student_obj.room = new_room
        old_room.save()
        new_room.save()
        student_obj.save()
        if new_room.capacity < old_room.capacity:
            msg='You will have to pay an extra amount.Please contact your warden immediately'
        else:
            msg = 'Regards'
        app.delete()
        transaction.commit()
        subject = 'Your request has been approved'
        message = 'Your room change request has been approved by the warden.Login to see your new room.'
        message = message + msg
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [student_obj.student.email]
        send_mail(subject,message,email_from,recipient_list)
        return redirect('approval_list')

@login_required(login_url='/')
def approve_confirm_new(request,id):
    app = NewRegistration.objects.filter(requester__student__username=id).first()
    student_obj = Student.objects.get(student__username=id)
    new_room = app.new_room
    if new_room.present == new_room.capacity:
        app.delete()
        transaction.commit()
        subject = 'Your Request has been cancelled'
        message = 'Your request for that room has been cancelled by warden,it was already full'
        email_from=settings.EMAIL_HOST_USER
        recipient_list = [student_obj.student.email]
        send_mail(subject,message,email_from,recipient_list)
        return render(request,'administration/room_full.html')
    else:
        new_room.present = new_room.present + 1
        student_obj.room = new_room
        new_room.save()
        student_obj.save()
        app.delete()
        transaction.commit()
        subject = 'Your request has been approved'
        message = 'Your new room has been approved by the warden.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [student_obj.student.email]
        send_mail(subject,message,email_from,recipient_list)
        return redirect('new_approval_list')

@login_required(login_url='/')
def approve_reject(request,id):
    if request.method == "POST":
        form = RejectForm(request.POST)
        if form.is_valid():
            msg = request.POST.get('message')
            app = RoomChange.objects.filter(requester__student__username=id).first()
            student_obj = Student.objects.get(student__username = id)
            subject = 'Your request for room has been rejected'
            message = 'Your room change request has been cancelled by warden.Reason:'
            message = message + msg
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [student_obj.student.email]
            send_mail(subject,message,email_from,recipient_list)
            app.delete()
            transaction.commit()
            return redirect('approval_list')
        else:
            form = RejectForm()
            context={
                'form':form,
                'username':id,
            }
            return render(request,'administration/reject_approval.html',context)
    else:
        form = RejectForm()
        context = {
            'form':form,
            'username':id,
        }
        return render(request,'administration/reject_approval.html',context)

@login_required(login_url='/')
def approve_reject_new(request,id):
    if request.method == "POST":
        form = RejectForm(request.POST)
        if form.is_valid():
            msg = request.POST.get('message')
            app = NewRegistration.objects.filter(requester__student__username = id).first()
            student_obj = Student.objects.get(student__username = id)
            subject = 'Your request has been rejected'
            message = 'Your new room selection has been rejected by warden.Reason:'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [student_obj.student.email]
            send_mail(subject,message,email_from,recipient_list)
            app.delete()
            return redirect('new_approval_list')
        else:
            form = RejectForm()
            context={
                'form':form,
                'username':id,
            }
            return render(request,'administration/reject_approval_new.html',context)
    else:
        form = RejectForm()
        context = {
            'form': form,
            'username': id,
        }
        return render(request, 'administration/reject_approval_new.html', context)

@login_required(login_url='/')
def fee_student_history(request):
    fee = Fee.objects.select_related('student').select_related('student__student').all()
    fee_data = []
    for i in fee:
        y={
            'student_name':i.student.student_name,
             'scholar_number':i.student.scholar_number,
            'course':i.student.course,
            'branch':i.student.branch,
            'date':i.date_paid,
            'approve':i.is_approved,
            'amount':i.amount,
        }
        fee_data.append(y)
    context = {
        'fee_data':fee_data,
    }
    return render(request,'administration/feehistory.html',context)

@login_required(login_url='/')
def fee_instructions(request):
    try:
        s = Fee.objects.get(student__student__username=request.user)
        return render(request,'administration/already.html')
    except:
        try:
            student_obj = Student.objects.get(student__username = request.user)
            room = student_obj.room
            room_type = room.room_type
            if room_type == 'S':
                amount = 15000
            elif room_type == 'D':
                amount = 12000
            else:
                amount = 9000
            context={'student_obj':student_obj,'amount':amount}
            return render(request,'administration/feepay.html',context)
        except:
            return render(request,'administration/room_before_fee.html')

@login_required(login_url='/')
def fee_register(request,id):
    if request.method == "POST":
        receipt = request.FILES.get('receipt')
    current_user = request.user
    student_obj= Student.objects.get(student=current_user)
    new_fee = Fee(
        student = student_obj,
        amount=id,
    )
    new_fee.save()
    fee_register = FeeRegister(
        fee=new_fee,
        receipt=receipt,
    )
    fee_register.save()
    return render(request, 'administration/request.html')

@login_required(login_url='/')
def fee_approval_list(request):
    fee = Fee.objects.all()
    print(fee)
    fee_data=[]
    for x in fee:
        if x.is_approved == False:
            fee_r = FeeRegister.objects.get(fee = x)
            print('fee register object is:',fee_r)
            l={
                'student_name':x.student.student_name,
                'course':x.student.course,
                'branch':x.student.branch,
                 'receipt':fee_r.receipt,
                'scholar_number':x.student.scholar_number,
                'date':x.date_paid,
                'username':x.student.student.username,
                'amount':x.amount,
            }
            fee_data.append(l)
    context={
        'fee_data':fee_data,
    }
    return render(request,'administration/fee_approval_list.html',context)

@login_required(login_url='/')
def fee_approval_confirm(request,id):
    fee = Fee.objects.filter(student__student__username = id).first()
    student_obj = Student.objects.get(student__username=id)
    fee.is_approved = True
    student_obj.fee_paid = True
    student_obj.save()
    fee.save()
    transaction.commit()
    subject = 'Your Fee Payment  has been approved by the warden'
    message = 'Your fee payment has been approved by the warden.Login to see your fee status'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [student_obj.student.email]
    send_mail(subject,message,email_from,recipient_list)
    return redirect('fee_approval_list')

@login_required(login_url='/')
def fee_approval_reject(request,id):
    if request.method=="POST":
        form = RejectForm(request.POST)
        if form.is_valid():
            msg =request.POST.get('message')
            fee = Fee.objects.filter(student__student__username = id).first()
            student_obj = Student.objects.get(student__username = id)
            fee_register = FeeRegister.objects.get(fee = fee)
            subject = 'Your fee payment has been rejected'
            message = 'Your Fee payment has been rejected by the warden.Reason:'
            message = message+msg
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [student_obj.student.email]
            send_mail(subject,message,email_from,recipient_list)
            fee_register.delete()
            fee.delete()
            transaction.commit()
            return redirect('fee_approval_list')
        else:
            username = id
            form = RejectForm()
            return render(request, 'administration/reject_approve_fee.html', {'username': username, 'form': form})
    else:
        username = id
        form = RejectForm()
        return render(request, 'administration/reject_approve_fee.html', {'username': username, 'form': form})

@login_required(login_url='/')
def fee_status(request):
    try:
        print(request.user)
        fee = Fee.objects.get(student__student = request.user)
        print(fee.student.student_name,fee.student.scholar_number)
        context={
            'student_name': fee.student.student_name,
            'scholar_number':fee.student.scholar_number,
            'course' : fee.student.course,
            'branch':fee.student.branch,
            'course_year':fee.student.course_year,
            'date':fee.date_paid,
            'fees':fee.is_approved,
            'amount':fee.amount,
        }
        return render(request,'administration/feeStatus.html',context)
    except:
        return render(request,'administration/noFee.html')

@login_required(login_url='/')
def student_leave_list(request):
    student_leave = StudentLeave.objects.all()
    context={
        'student_leave':student_leave,
    }
    print(context)
    return render(request,'administration/student_leave_list.html',context)

@login_required(login_url='/')
def student_leave_approve(request,id): #id is scholar_number
    student_leave = StudentLeave.objects.filter(student__scholar_number = id,status=0).first()
    print(student_leave.student.scholar_number)
    student_leave.status = 1
    student_leave.save()
    return  redirect('student_leave_list')

@login_required(login_url='/')
def student_leave_reject(request,id):
    student_leave = StudentLeave.objects.filter(student__scholar_number = id,status=0).first()
    print(student_leave.student.scholar_number)
    student_leave.status = 2
    student_leave.save()
    return redirect('student_leave_list')

@login_required(login_url='/')
def complaints_list(request):
    student_complaint = Complaint.objects.all()
    context={
        'student_complaint':student_complaint,
    }
    return render(request,'administration/student_complaint_list.html',context)

@login_required(login_url='/')
def complaints_reply(request,id):
    c = Complaint.objects.get(id=id)
    if request.method=="POST":
        reply = request.POST.get('reply')
    c.reply=reply
    c.save()
    return redirect('complaints_list')

@login_required(login_url='/')
def student_checkout_accept(request,id):
    checkout = Checkout.objects.get(id = id)
    checkout.is_accepted = 1
    checkout.save()
    return redirect('student_checkout_list')

@login_required(login_url='/')
def student_checkout_reject(request,id):
    checkout = Checkout.objects.get(id = id)
    checkout.is_accepted = 2
    checkout.save()
    return redirect('student_checkout_list')

@login_required(login_url='/')
def expense_list(request):
    expense = Expenses.objects.all()
    context={
        'expense':expense,
    }
    return render(request,'administration/expense_list.html',context)

@login_required(login_url='/')
def date_to_date_report(request):
    return render(request,'administration/date_to_date_report.html')

@login_required(login_url='/')
def get_report(request):
    try:
        if request.method == "POST":
            form = ReportForm(request.POST)
            if form.is_valid():
                from_date = request.POST.get('from_date')
                to_date = request.POST.get('to_date')
                fee = Fee.objects.filter(date_paid__range=[from_date, to_date])
                total_fee = fee.aggregate(total=Sum('amount'))
                print(total_fee)
                expense = Expenses.objects.filter(date__range=[from_date, to_date])
                total_expense = expense.aggregate(total=Sum('amount'))
                print(total_expense)
                if total_expense['total']== None:
                    total_expense['total'] = 0
                if total_fee['total']==None:
                    total_fee['total']=0
                profit = total_fee['total'] - total_expense['total']
                dict_p = {
                    'total': profit
                }
                context = {
                    'total_fee': total_fee['total'],
                    'total_expense': total_expense['total'],
                    'dict_p': dict_p['total'],
                }
                return render(request, 'administration/report.html', context)
            else:
                form = ReportForm()
                return render(request, 'administration/date_to_date_report.html', {'form': form})

        else:
            form = ReportForm()
            return render(request, 'administration/date_to_date_report.html', {'form': form})
    except:
        return render(request,'administration/not_present.html')


