from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import *
import datetime

# Company Render pages

def departments(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please log in to view page')
    user = User.objects.get(id=request.session['user_id'])
    if user.level == 0:
        messages.error(request, 'You are not authorized to view this page')
        return redirect('/')
    else:
        company = Company.objects.get(owner_id=request.session['user_id'])
        departments = Department.objects.filter(company_id=company.id)
        context = {
            'user': user,
            'company': company,
            'departments': departments,
        }
        messages.success(request, f'{user.firstName}')
        return render(request, 'owner/departments.html', context)

def payRates(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please log in to view page')
    user = User.objects.get(id=request.session['user_id'])
    if user.level == 0:
        messages.error(request, 'You are not authorized to view this page')
        return redirect('/')
    else:
        company = Company.objects.get(owner_id=request.session['user_id'])
        rates = PayRate.objects.filter(co_id=company.id)
        context = {
            'user': user,
            'company': company,
            'rates': rates,
        }
        messages.success(request, f'{user.firstName}')
        return render(request, 'owner/payRate.html', context)

def managers(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please log in to view page')
    user = User.objects.get(id=request.session['user_id'])
    if user.level == 0:
        messages.error(request, 'You are not authorized to view this page')
        return redirect('/')
    else:
        company = Company.objects.get(owner_id=request.session['user_id'])
        departments = Department.objects.filter(company_id=company.id)
        payRates = PayRate.objects.filter(co_id=company.id)
        managers = Management.objects.filter(theCo_id=company.id)
        users = User.objects.filter(workFor=company.id)
        context = {
            'user': user,
            'company': company,
            'departments': departments,
            'payRates': payRates,
            'managers': managers,
            'users': users,
        }
        messages.success(request, f'{user.firstName}')
        return render(request, 'owner/managers.html', context)

def employees(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please log in to view page')
    user = User.objects.get(id=request.session['user_id'])
    if user.level == 0:
        messages.error(request, 'You are not authorized to view this page')
        return redirect('/')
    else:
        company = Company.objects.get(owner_id=request.session['user_id'])
        departments = Department.objects.filter(company_id=company.id)
        payRates = PayRate.objects.filter(co_id=company.id)
        employees = Employee.objects.filter(theCompany_id=company.id)
        users = User.objects.filter(theData=company.id)
        context = {
            'user': user,
            'company': company,
            'departments': departments,
            'payRates': payRates,
            'employees': employees,
            'users': users,
        }
        print(employees)
        messages.success(request, f'{user.firstName}')
        return render(request, 'owner/employees.html', context)

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
        company = Company.objects.get(owner_id=request.session['user_id'])
        context = {
            'user': user,
            'company': company,
        }
        print(company)
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
        company = Company.objects.get(owner_id=request.session['user_id'])
        context = {
            'user': user,
            'company': company,
        }
        messages.success(request, f'{user.firstName}')
        return render(request, 'owner/addPay.html', context)

def addManager(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please log in to view page')
    user = User.objects.get(id=request.session['user_id'])
    payRates = PayRate.objects.all().values()
    departments = Department.objects.all().values()
    company = Company.objects.get(owner_id=request.session['user_id'])
    if user.level == 2:
        context = {
            'user': user,
            'payRates': payRates,
            'departments': departments,
            'company': company,
        }
        print(company)
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
    company = Company.objects.get(owner_id=request.session['user_id'])
    if user.level == 2:
        context = {
            'user': user,
            'payRates': payRates,
            'departments': departments,
            'company': company,
        }
        print(company)
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

def companyCodes(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please login")
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    if user.level == 0:
        messages.error(request, 'You are not authorized to view this page')
        return redirect('/dashboard/')
    else:
        codes = UserCodes.objects.filter(creator_id=request.session['user_id'])
        company = Company.objects.get(owner_id=request.session['user_id'])
        users = User.objects.all().values()
        context = {
            'user': user,
            'codes': codes,
            'users': users,
            'company': company,
        }
        messages.success(request, f'{user.firstName}')
        return render(request, 'owner/codes.html', context)

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
    messages.success(request, 'Department Created')
    return redirect('/company/departments/')

def createPayRate(request):
    PayRate.objects.create(
        rate=request.POST['rate'],
        level=request.POST['level'],
        co_id=request.POST['co']
    )
    messages.success(request, 'Pay Rate Created')
    return redirect('/company/payRates/')

def createManager(request):
    Management.objects.create(
        firstName=request.POST['firstName'],
        lastName=request.POST['lastName'],
        email=request.POST['email'],
        hireDate=request.POST['hireDate'],
        terminated=0,
        title=request.POST['title'],
        pay_id=request.POST['pay'],
        dept_id=request.POST['dept'],
        theCo_id=request.POST['theCo']
    )
    messages.success(request, 'Manager Added')
    return redirect('/company/managers/')

def createEmployee(request):
    Employee.objects.create(
        firstName=request.POST['firstName'],
        lastName=request.POST['lastName'],
        email=request.POST['email'],
        hireDate=request.POST['hireDate'],
        terminated=0,
        title=request.POST['title'],
        payRate_id=request.POST['payRate'],
        department_id=request.POST['department'],
        theCompany_id=request.POST['theCompany']
    )
    messages.success(request, 'Employee Added')
    return redirect('/company/employees/')

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