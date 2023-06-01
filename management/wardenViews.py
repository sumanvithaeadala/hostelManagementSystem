from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from management.models import Course,year,Student,CustomUser,Room,Warden,NewRegistration,Fee,RoomChange,FeeRegister,StudentLeave,Complaint,Checkout,Expenses
from django.contrib import messages

@login_required(login_url='/')
def home(request):
    return render(request,'warden/home.html')

@login_required(login_url='/')
def add_expense(request):
    return render(request,'administration/addExpense.html')

@login_required(login_url='/')
def save_expense(request):
    if request.method == "POST":
        warden_name = request.POST.get('warden_name')
        type = request.POST.get('type')
        amount = request.POST.get('amount')
        receipt=request.FILES.get('receipt')
    warden_obj = Warden.objects.get(warden_name = warden_name)
    expense = Expenses(
        warden = warden_obj,
        type = type,
        amount = amount,
        receipt=receipt,
    )
    expense.save()
    messages.success(request,'Expense added successfully')
    return render(request,'administration/addExpense.html')