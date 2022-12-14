from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.index),
    path('logreg/', views.logReg),
    path('login/', views.login),
    path('reg/', views.reg),
    path('logout/', views.logout),
    path('dashboard/', views.dashboard),

    # Admin Routes
    path('theAdmin/codes/', views.allCodes),
    path('theAdmin/generateCode/', views.generateCode),
    path('theAdmin/companies/', views.allCompanies),
    path('theAdmin/users/', views.allUsers),

    # Management Routes
    path('company/add/', views.addCompany),
    path('company/create/', views.createCompany),
    path('company/codes/', views.companyCodes),
    path('company/generateCode/', views.generateCode),
    path('company/departments/', views.departments),
    path('company/department/add/', views.addDepartment),
    path('company/department/create/', views.createDepartment),
    path('company/payRates/', views.payRates),
    path('company/payRate/add/', views.addPayRate),
    path('company/payRate/create/', views.createPayRate),
    path('company/managers/', views.managers),
    path('company/manager/add/', views.addManager),
    path('company/manager/create/', views.createManager),
    path('company/employees/', views.employees),
    path('company/employee/add/', views.addEmployee),
    path('company/employee/create/', views.createEmployee),
]