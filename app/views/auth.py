from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import *
from app.key import *
import bcrypt
import datetime

# ############ Render pages

def index(request):
    if 'user_id' not in request.session:
        return render(request, 'index.html')
    return render(request, 'altIndex.html')

def logReg(request):
    if 'user_id' not in request.session:
        return render(request, 'logReg.html')
    else:
        return redirect('/dashboard/')

# ############ Log/Reg Functions

def logout(request):
    request.session.clear()
    messages.info(request, 'You have been logged out')
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
    print('the new user:', newUser)
    request.session['user_id'] = newUser.id
    if newUser.id == 1:
        toUpdate = User.objects.get(id=request.session['user_id'])
        toUpdate.level=24
        toUpdate.save()
        messages.success(request, "Welcome Admin Member")
        return redirect('/dashboard/')
    if request.POST['regcode'] == SUPERADMINKEY:
        toUpdate = User.objects.get(id=request.session['user_id'])
        toUpdate.level=24
        toUpdate.save()
        messages.success(request, "Welcome Admin User")
        return redirect('/dashboard/')
    codes = UserCodes.objects.all().values()
    print('the codes:', codes)
    for code in codes:
        if request.POST['role'] == 'owner':
            if request.POST['regcode'] == code['userCode']:
                toUpdate = User.objects.get(id=request.session['user_id'])
                toUpdate.level=2
                toUpdate.save()
                messages.success(request, "Welcome Owner")
                codeUsed = UserCodes.objects.get(id=code['id'])
                codeUsed.lastUsed = datetime.datetime.now()
                codeUsed.save()
                return redirect('/dashboard/')
        if request.POST['role'] == 'manager':
            if request.POST['regcode'] == code['userCode']:
                toUpdate = User.objects.get(id=request.session['user_id'])
                toUpdate.level=1
                toUpdate.save()
                messages.success(request, "Welcome HR")
                codeUsed = UserCodes.objects.get(id=code['id'])
                codeUsed.lastUsed = datetime.datetime.now()
                codeUsed.save()
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
        # Checking user level
        # Super Admin == 24
        if user.level == 24:
            context = {
                'user': user,
                'companies': companies,
                'employees': employees,
                'managers': managers
            }
            messages.success(request, f"Welcome Admin User {user.firstName}")
            return render(request, 'admin/adminDash.html', context)
        # Owner == 2
        if user.level == 2:
            # Checking if owner has a Company attached 0 = No
            print('createdAt', user.createdAt, 'updatedAt', user.updatedAt)
            if user.workFor == 0:
                context = {
                    'user': user,
                }
                messages.success(request, f"Welcome Owner {user.firstName}")
                return render(request, 'owner/ownerDash.html', context)
            # Assumes that the user is a return user and has data attached already
            company = Company.objects.get(id=user.workFor)
            context = {
                'user': user,
                'company': company
            }
            messages.success(request, f'Welcome {user.firstName}')
            return render(request, 'owner/ownerDash.html', context)
        # Hr == 1
        if user.level == 1:
            if user.theData == 0:
                for m in managers:
                    if user.email == m['email']:
                        toUpdate=User.objects.get(id=user.id)
                        toUpdate.theData=m['id']
                        for c in companies:
                            if m['theCo_id'] == c['id']:
                                toUpdate.workFor=c['id']
                                toUpdate.save()
                company = Company.objects.filter(id=user.workFor)
                manager = Management.objects.filter(id=user.theData)
                context = {
                    'user': user,
                    'manager': manager,
                    'company': company
                }
                messages.success(request, f'Welcome {user.firstName}')
                return render(request, 'hr/hrDash.html', context)
            company = Company.objects.filter(id=user.workFor)
            manager = Management.objects.filter(id=user.theData)
            context = {
                'user': user,
                'manager': manager,
                'company': company
                }
            messages.success(request, f'Welcome {user.firstName}')
            return render(request, 'hr/hrDash.html', context)
        # General Member
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
def profile(request):
    pass

def editProfile(request):
    pass

# ############ Profile Create Functions
def createProfile(request):
    pass

# ############ Profile Update Functions
def updateProfile(request):
    pass

def allowGenCode(request):
    pass

# ############ Profile Delete Functions
