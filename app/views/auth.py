from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import *
from app.key import *
import bcrypt
import datetime

# ############ Render pages

def index(request):
    return render(request, 'index.html')

def logReg(request):
    if 'user_id'  not in request.session:
        return render(request, 'logReg.html')
    else:
        user = User.objects.get(id=request.session['user_id'])
        logs = Log.objects.all().order_by('-updatedAt')
        context = {
            'user': user,
            'logs': logs,
        }
        return render(request, 'index.html', context)

# ############ Log/Reg Functions

def logout(request):
    request.session.clear()
    messages.error(request, 'You have been logged out')
    return redirect('/')

def login(request):
    user = User.objects.filter(email = request.POST['email'])
    if user:
        userLogin = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), userLogin.password.encode()):
            request.session['user_id'] = userLogin.id
            toUpdate = User.objects.get(id=userLogin.id)
            toUpdate.loggedOn = datetime.datetime.now()
            toUpdate.save()
            return redirect('/dashboard/')
        messages.error(request, 'Invalid Credentials')
        return redirect('/logreg/')
    messages.error(request, 'That Email is not in our system, please register for an account')
    return redirect('/logreg/')

def reg(request):
    errors = User.objects.validate(request.POST)
    if errors:
        for err in errors.values():
            messages.error(request, err)
        return redirect('/logreg/')
    hashedPw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    newUser = User.objects.create(
        firstName = request.POST['firstName'],
        lastName = request.POST['lastName'],
        email = request.POST['email'],
        password = hashedPw
    )
    request.session['user_id'] = newUser.id
    if newUser.id == 1:
        toUpdate = User.objects.get(id=request.session['user_id'])
        toUpdate.level=24
        toUpdate.save()
        messages.error(request, "Welcome Admin Member")
        return redirect('/dashboard/')
    if request.POST['regcode'] == SUPERADMINKEY:
        toUpdate = User.objects.get(id=request.session['user_id'])
        toUpdate.level=24
        toUpdate.save()
        messages.error(request, "Welcome Admin User")
        return redirect('/dashboard/')
    if request.POST['regcode'] == OWNERKEY:
        toUpdate = User.objects.get(id=request.session['user_id'])
        toUpdate.level=2
        toUpdate.save()
        messages.error(request, "Welcome Owner")
        return redirect('/dashboard/')
    if request.POST['regcode'] == HRKEY:
        toUpdate = User.objects.get(id=request.session['user_id'])
        toUpdate.level=1
        toUpdate.save()
        messages.error(request, "Welcome HR")
        return redirect('/dashboard/')
    else:
        return redirect('/dashboard/')

# ############ Dashboard
def dashboard(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please log in to view this page')
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        companies = Company.objects.all().values()
        employees = Employee.objects.all().values()
        managers = Management.objects.all().values()
        if user.level == 24:
            context = {
                'user': user,
                'companies': companies,
                'employees': employees,
                'managers': managers
            }
            return render(request, 'adminDash.html', context)
        if user.level == 2:
            if user.theData == 0:
                for m in managers:
                    if user.email == m.email:
                        toUpdate=User.objects.get(id=user.id)
                        toUpdate.theData=m.id
                        for c in companies:
                            if m.theCo == c.id:
                                toUpdate.workFor=c.id
                                toUpdate.save()
                company = Company.objects.filter(id=user.workFor)
                manager = Management.objects.filter(id=user.theData)
                context = {
                    'user': user,
                    'manager': manager,
                    'company': company
                }
                return render(request, 'ownerDash.html', context)
            company = Company.objects.filter(id=user.workFor)
            manager = Management.objects.filter(id=user.theData)
            context = {
                'user': user,
                'manager': manager,
                'company': company
                }
            return render(request, 'ownerDash.html')
        if user.level == 1:
            if user.theData == 0:
                for m in managers:
                    if user.email == m.email:
                        toUpdate=User.objects.get(id=user.id)
                        toUpdate.theData=m.id
                        for c in companies:
                            if m.theCo == c.id:
                                toUpdate.workFor=c.id
                                toUpdate.save()
                company = Company.objects.filter(id=user.workFor)
                manager = Management.objects.filter(id=user.theData)
                context = {
                    'user': user,
                    'manager': manager,
                    'company': company
                }
                return render(request, 'hrDash.html', context)
            company = Company.objects.filter(id=user.workFor)
            manager = Management.objects.filter(id=user.theData)
            context = {
                'user': user,
                'manager': manager,
                'company': company
                }
            return render(request, 'hrDash.html', context)
        else:
            if user.theData == 0:
                for e in employees:
                    if user.email == e.email:
                        toUpdate=User.objects.get(id=user.id)
                        toUpdate.theData=e.id
                        for c in companies:
                            if e.theCompany == c.id:
                                toUpdate.workFor=c.id
                                toUpdate.save()
                employee = Employee.objects.filter(id=user.theData)
                company = Company.objects.filter(id=user.workFor)
                context = {
                    'user': user,
                    'employee': employee,
                    'company': company
                }
                return render(request, 'dashboard.html', context)
            employee = Employee.objects.filter(id=user.theData)
            company = Company.objects.filter(id=user.workFor)
            context = {
                'user': user,
                'employee': employee,
                'company': company
            }
            return render(request, 'dashboard.html', context)



# ############ Profile Render Functions

# ############ Profile Create Functions

# ############ Profile Update Functions

# ############ Profile Delete Functions