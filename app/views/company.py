from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import *
import datetime

# Company Render pages

def addCompany(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please log in to view page')
    user = User.objects.get(id=request.session['user_id'])
    if user.level != 2:
        messages.error(request, 'You are not authorized to view this page')
        return redirect('/')
    else:
        context = {
            'user': user,
        }
        messages.success(request, f'{user.firstName}')
        return render(request, 'owner/addCo.html', context)

def addDepartment(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please log in to view page')
    user = User.objects.get(id=request.session['user_id'])
    if user.level != 2:
        messages.error(request, 'You are not authorized to view this page')
        return redirect('/')
    else:
        company = Company.objects.filter(owner_id=request.session['user_id'])
        context = {
            'user': user,
            'company': company,
        }
        messages.success(request, f'{user.firstName}')
        return render(request, 'owner/addDept.html', context)

def addPayRate(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please log in to view page')
    user = User.objects.get(id=request.session['user_id'])
    if user.level != 2:
        messages.error(request, 'You are not authorized to view this page')
        return redirect('/')
    else:
        pay = PayRate.objects.filter(co_id=request.session['user_id'])
        context = {
            'user': user,
            'pay': pay,
        }
        messages.success(request, f'{user.firstName}')
        return render(request, 'owner/addPay.html', context)

def addManager(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please log in to view page')
    user = User.objects.get(id=request.session['user_id'])
    payRates = PayRate.objects.all().values()
    departments = Department.objects.all().values()
    company = Company.objects.filter(theCo_id=request.session['user_id'])
    if user.level == 2:
        context = {
            'user': user,
            'payRates': payRates,
            'departments': departments,
            'company': company,
        }
        messages.success(request, f'{user.firstName}')
        return render(request, 'owner/addManager.html', context)
    if user.level == 1:
        context = {
            'user': user,
            'payRates': payRates,
            'departments': departments,
            'company': company,
        }
        messages.success(request, f'{user.firstName}')
        return render(request, 'hr/addManager.html', context)
    else:
        messages.error(request, 'You are not authorized to view this page')
        return redirect('/')

def addEmployee(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please log in to view page')
    user = User.objects.get(id=request.session['user_id'])
    payRates = PayRate.objects.all().values()
    departments = Department.objects.all().values()
    company = Company.objects.filter(theCompany_id=request.session['user_id'])
    if user.level == 2:
        context = {
            'user': user,
            'payRates': payRates,
            'departments': departments,
            'company': company,
        }
        messages.success(request, f'{user.firstName}')
        return render(request, 'owner/addEmployee.html', context)
    if user.level == 1:
        
        context = {
            'user': user,
            'payRates': payRates,
            'departments': departments,
            'company': company,
        }
        messages.success(request, f'{user.firstName}')
        return render(request, 'hr/addEmployee.html', context)
    else:
        messages.error(request, 'You are not authorized to view this page')
        return redirect('/')

# Company Create Pages

def createCompany(request):
    Company.objects.create(
        name=request.POST['name'],
        address1=request.POST['address1'],
        address2=request.POST['address2'],
        city=request.POST['city'],
        state=request.POST['state'],
        zipCode=request.POST['zipCode'],
        owner=User.objects.get(id=request.session['user_id']),
    )
    messages.success(request, 'Company Created')
    return redirect('/dashboard/')

def createDepartment(request):
    Department.objects.create(
        name=request.POST['name'],
        company_id=request.POST['company']
    )

def createPayRate(request):
    PayRate.objects.create(
        rate=request.POST['rate'],
        co_id=request.POST['co']
    )

def createManager(request):
    Management.objects.create(
        firstName=request.POST['firstName'],
        lastName=request.POST['lastName'],
        email=request.POST['email'],
        hireDate=request.POST['hireDate'],
        promotionDate=request.POST['promotionDate'],
        lastPromotion=request.POST['lastPromotion'],
        terminationDate='',
        terminated=0,
        title=request.POST['title'],
        pay_id=request.POST['pay'],
        dept_id=request.POST['dept'],
        theCo_id=request.POST['theCo']
    )

def createEmployee(request):
    pass

# Company View Pages

def viewEmployees(request):
    pass

def viewEmployee(request):
    pass

def editCompany(request):
    pass

def editDepartment(request):
    pass

def editPayRate(request):
    pass

def editManager(request):
    pass

def editEmployee(request):
    pass


# Company Edit pages


# Company Delete Pages