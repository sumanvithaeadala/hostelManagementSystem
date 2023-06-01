from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from management.models import Course,year,Student,CustomUser,Room,Warden,NewRegistration,Fee,RoomChange,FeeRegister,StudentLeave,Complaint,Checkout
from django.contrib import messages

@login_required(login_url='/')
def home(request):
    return render(request,'student/home.html')

@login_required(login_url='/')
def student_leave(request):
        return render(request, 'administration/studentLeave.html')

@login_required(login_url='/')
def student_leave_save(request):
    if request.method == "POST":
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        reason = request.POST.get('reason')
        ticket = request.FILES.get('ticket')
    student_obj = Student.objects.get(student__username = request.user)
    student_leave = StudentLeave(
        student = student_obj,
        from_date = from_date,
        to_date = to_date,
        message = reason,
        ticket = ticket,
    )
    student_leave.save()
    messages.success(request,'Leave application submitted successfully')
    return redirect('student_leave')

@login_required(login_url='/')
def student_leave_history(request):
    student_leave = StudentLeave.objects.filter(student__student__username = request.user)
    context={
        'student_leave':student_leave,
    }
    print(context)
    return render(request,'administration/leave_history.html',context)

@login_required(login_url='/')
def student_complaint(request):
    return render(request,'administration/student_complaint.html')

@login_required(login_url='/')
def student_complaint_save(request):
    if request.method == "POST":
        message = request.POST.get('message')
    current_user = Student.objects.get(student__username = request.user)
    c = Complaint(
        student = current_user,
        message = message,
    )
    c.save()
    messages.success(request,'complaint submitted successfully')
    return redirect('student_complaint')

@login_required(login_url='/')
def complaint_history(request): #once check this will be visible to all students or individual
    c = Complaint.objects.filter(student__student__username = request.user)
    context={
        'c':c,
    }
    return render(request,'administration/complaint_history.html',context)


@login_required(login_url='/')
def student_checkout(request):
    return render(request,'administration/student_checkout.html')

@login_required(login_url='/')
def student_checkout_save(request):
    try:
        s = Checkout.objects.get(student__student__username = request.user)
        return render(request,'administration/already.html')
    except:
        if request.method == "POST":
            date = request.POST.get('date')
        student_obj = Student.objects.get(student__username=request.user)
        sobj = Checkout(
            student=student_obj,
            date=date,
        )
        sobj.save()
        messages.success(request,'Your application for Checkout is submitted successfully')
        return render(request, 'administration/student_checkout.html')


@login_required(login_url='/')
def student_checkout_status(request):
    c = Checkout.objects.get(student__student__username = request.user)
    context={
        'c':c,
    }
    return render(request,'administration/checkout_status.html',context)

@login_required(login_url='/')
def student_checkout_list(request):
    checkout = Checkout.objects.all()
    context={
        'checkout':checkout,
    }
    return render(request,'administration/checkout_list.html',context)

@login_required(login_url='/')
def close_complaint(request,id):
    c = Complaint.objects.get(id = id)
    print(c.reply)
    print(c.id)
    c.status = True
    c.save()
    return redirect('complaint_history')






