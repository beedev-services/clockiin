from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import *
import datetime
import string
import random

def allCodes(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please login")
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    if user.level != 24:
        messages.error(request, 'You are not authorized to view this page')
        return redirect('/dashboard/')
    else:
        codes = UserCodes.objects.all().values()
        companies = Company.objects.all().values()
        users = User.objects.all().values()
        context = {
            'user': user,
            'codes': codes,
            'users': users,
            'companies': companies,
        }
        messages.success(request, f'{user.firstName}')
        return render(request, 'admin/codes.html', context)

def allCompanies(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please login")
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    if user.level != 24:
        messages.error(request, 'You are not authorized to view this page')
        return redirect('/dashboard/')
    else:
        companies = Company.objects.all().values()
        users = User.objects.all().values()
        context = {
            'user': user,
            'companies': companies,
            'users': users,
        }
        messages.success(request, f'{user.firstName}')
        return render(request, 'admin/companies.html', context)

def allUsers(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please login")
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    if user.level != 24:
        messages.error(request, 'You are not authorized to view this page')
        return redirect('/dashboard/')
    else:
        users = User.objects.all().values()
        mUsers = User.objects.filter(level=1)
        eUsers = User.objects.filter(level=0)
        managers = Management.objects.all().values()
        employees = Employee.objects.all().values()
        companies = Company.objects.all().values()
        context = {
            'user': user,
            'users': users,
            'managers': managers,
            'companies': companies,
            'employees': employees,
            'mUsers': mUsers,
            'eUsers': eUsers,
        }
        messages.success(request, f'{user.firstName}')
        return render(request, 'admin/users.html', context)

def generateCode(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please login")
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    if user.level == 24:
        N = 12
        res = ''.join(random.choices(string.ascii_letters, k=N))
        code = str(res)
        UserCodes.objects.create(
            userCode=code,
            creator=user,
        )
        messages.success(request, f'Owner Registration Code {code} Generated')
        return redirect('/theAdmin/codes/')
    N = 8
    res = ''.join(random.choices(string.ascii_letters, k=N))
    print("The generated random string : " + str(res))
    code = str(res)
    user = User.objects.get(id=request.session['user_id'])
    UserCodes.objects.create(
        userCode=code,
        creator=user
    )
    messages.success(request, f'{code} Generated')
    return redirect('/company/codes/')
