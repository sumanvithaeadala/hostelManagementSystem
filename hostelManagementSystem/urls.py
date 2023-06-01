"""hostelManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from management import studentViews,wardenViews,administrationViews,views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/',views.base,name='base'),
    path('administration/invalid', views.invalid, name='invalid'),#It give header,footer and sidebar.we extend other html pages using this so that we get same outline for every page

    #login paths
    path('',views.Login,name='Login'), #It is our main page
    path('doLogin',views.doLogin,name='doLogin'),
    path('doLogout',views.doLogout,name='doLogout'),
    path('register',views.register,name='register'),

    #passsword reset urls
    path('password/forgot/',views.forget_password,name='forget_password'),
    path('password/change/<str:token>',views.change_password,name='change_password'),

    # This is administration panel URLs
    path('administration/home',administrationViews.home,name='administrationHome'),
    path('administration/student/add',administrationViews.addStudent,name='add_student'),
    path('administration/student/list',administrationViews.studentlist,name='studentlist'),
    path('administration/student/edit/<str:id>',administrationViews.edit_student,name='edit_student'),
    path('administration/student/update',administrationViews.update_student,name='update_student'),
    path('administration/student/delete/<str:student>',administrationViews.delete_student,name='delete_student'),#admin is id of customuser,if we delete user,student willl be deleted automatically
    path('administration/student/details/<str:id>',administrationViews.student_details,name='student_details'),




    #room
    path('administration/room/add',administrationViews.add_room,name='add_room'),
    path('administration/room/list',administrationViews.roomlist,name='roomlist'),
    path('administration/room/select/<str:id>',administrationViews.selectRoom,name='selectRoom'),
    path('administration/room/student/<str:id>',administrationViews.roomDetails,name='roomDetails'),
    path('administration/room/list_aw',administrationViews.roomlist_aw,name='roomlist_aw'),
    path('administration/room/Change',administrationViews.room_change_view,name='room_change'),
    path('administration/room/change/approval/<str:id>', administrationViews.room_change_approval, name='room_change_approval'),
    path('administration/room/approvalList', administrationViews.approve_all_view_warden, name='approval_list'),
    path('administration/room/approvalList_new',administrationViews.new_approve_all_view_warden, name='new_approval_list'),
    path('administration/room/approval/confirm/<str:id>', administrationViews.approve_confirm, name='approve_confirm'),
    path('administration/room/approval_new/confirm/<str:id>', administrationViews.approve_confirm_new, name='approval_confirm_new'),
    path('administration/room/approval/reject/<str:id>', administrationViews.approve_reject, name='approve_reject'),
    path('administration/room/approval_new/reject/<str:id>', administrationViews.approve_reject_new, name='approve_reject_new'),

    #warden
    path('administration/warden/add',administrationViews.add_warden,name='add_warden'),
    path('administration/warden/list',administrationViews.wardenlist,name='wardenlist'),
    path('administration/warden/edit/<str:warden>',administrationViews.edit_warden,name='edit_warden'),
    path('administration/warden/update',administrationViews.update_warden,name='update_warden'),
    path('administration/warden/delete/<str:id>',administrationViews.delete_warden,name='delete_warden'),
    path('administration/warden/details/<str:id>',administrationViews.warden_details,name='warden_details'),

     #fee
    path('administration/fee/history', administrationViews.fee_student_history, name='fee_history'),
    path('administration/fee/pay', administrationViews.fee_instructions, name='fee_pay'),
    path('administration/fee/register/<str:id>',administrationViews.fee_register, name='fee_register'),
    path('administration/fee/approval/list', administrationViews.fee_approval_list, name='fee_approval_list'),
    path('administration/fee/approval/confirm/<str:id>', administrationViews.fee_approval_confirm,name='fee_approval_confirm'),
    path('administration/fee/approval/reject/<str:id>', administrationViews.fee_approval_reject,name='fee_approval_reject'),
    path('administration/fee/status', administrationViews.fee_status, name='fee_status'),

    path('administration/student/leave_list',administrationViews.student_leave_list,name = 'student_leave_list'),
    path('administration/student/leave/confirm/<str:id>',administrationViews.student_leave_approve,name='student_leave_approve'),
    path('administration/student/leave/reject/<str:id>', administrationViews.student_leave_reject,name='student_leave_reject'),

   path('administration/student/complaint/list',administrationViews.complaints_list,name="complaints_list"),
    path('administration/student/complaint/reply/<str:id>', administrationViews.complaints_reply,name="complaints_reply"),
    path('student/checkout/accept/<str:id>', administrationViews.student_checkout_accept, name='student_checkout_accept'),
    path('student/checkout/reject/<str:id>', administrationViews.student_checkout_reject, name='student_checkout_reject'),

     path('expense/list',administrationViews.expense_list,name='expense_list'),

      path('administration/date_to_date_report',administrationViews.date_to_date_report,name='date_to_date_report'),
    path('administration/get_report', administrationViews.get_report,
                       name='get_report'),

     path('administration/admin/add',administrationViews.add_admin,name='add_admin'),
     path('administration/admin/list',administrationViews.admin_list,name='admin_list'),
     path('administration/admin/edit/<str:admin>',administrationViews.edit_admin,name='edit_admin'),
     path('administration/admin/update',administrationViews.update_admin,name='update_admin'),
     path('administration/admin/details/<str:id>',administrationViews.admin_details,name = 'admin_details'),
     path('administration/admin/delete/<str:id>',administrationViews.delete_admin,name='delete_admin'),
    #profile update
    path('profile',views.profile,name='profile'),
    path('profile/update',views.updateProfile,name='update_profile'),

    #Staff URLs
    path('warden/home',wardenViews.home,name='wardenHome'),

    #Student URLs
       path('student/home',studentViews.home,name='studentHome'),
       path('student/leave', studentViews.student_leave, name='student_leave'),
       path('student/leave/save', studentViews.student_leave_save, name='student_leave_save'),
       path('student/leave/history', studentViews.student_leave_history, name='student_leave_history'),
       path('student/complaint',studentViews.student_complaint,name='student_complaint'),
       path('student/complaint/save',studentViews.student_complaint_save,name='student_complaint_save'),
       path('student/complaint/history',studentViews.complaint_history,name='complaint_history'),
       path('student/complaint/close/<str:id>',studentViews.close_complaint,name='close_complaint'),

       path('student/checkout',studentViews.student_checkout,name='student_checkout'),
       path('student/checkout/status',studentViews.student_checkout_status,name='student_checkout_status'),
       path('student/checkout/save',studentViews.student_checkout_save,name='student_checkout_save'),
       path('student/checkout/list',studentViews.student_checkout_list,name='student_checkout_list'),

       path('warden/expense/add',wardenViews.add_expense,name='add_expense'),
       path('warden/expense/save',wardenViews.save_expense,name='save_expense'),

              ]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
