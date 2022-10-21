from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import *
from app.regcodes import *
import bcrypt
import datetime

# ############ Render pages

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
    return redirect('/logReg/')

def login(request):
    user = User.objects.filter(username = request.POST['username'])
    if user:
        userLogin = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), userLogin.password.encode()):
            request.session['user_id'] = userLogin.id
            toUpdate = User.objects.get(id=userLogin.id)
            toUpdate.loggedOn = datetime.datetime.now()
            toUpdate.save()
            if userLogin.level == 2:
                return redirect('/ownerDash/')
            if userLogin.level == 1:
                return redirect('/hrDash/')
            if userLogin.level == 24:
                return redirect('/adminDash/')
            else:
                return redirect('/')
        messages.error(request, 'Invalid Credentials')
        return redirect('/logReg/')
    messages.error(request, 'That Username is not in our system, please register for an account')
    return redirect('/logReg/')

def register(request):
    errors = User.objects.validate(request.POST)
    if errors:
        for err in errors.values():
            messages.error(request, err)
        return redirect('/logReg/')
    hashedPw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    newUser = User.objects.create(
        firstName = request.POST['firstName'],
        lastName = request.POST['lastName'],
        username = request.POST['username'],
        email = request.POST['email'],
        password = hashedPw
    )
    request.session['user_id'] = newUser.id
    if newUser.id == 1:
        toUpdate = User.objects.get(id=request.session['user_id'])
        toUpdate.level=24
        toUpdate.save()
        messages.error(request, "Welcome Admin Member")
        return redirect('/adminDash/')
    if request.POST['REGCODE'] == OWNERKEY:
        toUpdate = User.objects.get(id=request.session['user_id'])
        toUpdate.level=2
        toUpdate.save()
        messages.error(request, "Welcome Owner")
        return redirect('/ownerDash/')
    if request.POST['REGCODE'] == HRKEY:
        toUpdate = User.objects.get(id=request.session['user_id'])
        toUpdate.level=1
        toUpdate.save()
        messages.error(request, "Welcome HR")
        theList = Management.objects.all().values()
        for company in theList:
            if request.POST['email'] == company.email:
                toUpdate = User.objects.get(id=request.session['user_id'])
                toUpdate.employer=company.company_id
                toUpdate.save()
                messages.error(request, "Email recognized and company added to profile")
                return redirect('/hrDash/')
    if request.POST['role'] == 'Employee':
        theList = Employee.objects.all().values()
        for company in theList:
            if request.POST['email'] == company.email:
                toUpdate = User.objects.get(id=request.session['user_id'])
                toUpdate.employer=company.company_id
                toUpdate.save()
                messages.error(request, "Email recognized and company added to profile")
                return redirect('/')

# ############ Profile Render Functions

# ############ Profile Create Functions

# ############ Profile Update Functions

# ############ Profile Delete Functions