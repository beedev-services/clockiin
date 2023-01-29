from django.db import models
from django.core.validators import RegexValidator
import re
from django.db.models.fields import BooleanField, CharField
from django.db.models.signals import post_save
from django.db.models.deletion import CASCADE
import datetime
from .key import *

class UserManager(models.Manager):
    def validate(self, form):
        errors = {}
        # Email format
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # Pulling emails
        emailCheck = self.filter(email=form['email'])
        # Creating list of employee emails
        employees = []
        employeeList = Employee.objects.all().values()
        for e in employeeList:
            employees.append(e['email'])
        # Pulling Created Reg Codes
        codes = []
        codeList = UserCodes.objects.all().values()
        print('the code list', codeList)
        for c in codeList:
            # print('one row in codelist', c)
            codes.append(c['userCode'])
            # print('one code', c['userCode'], 'the id', c['id'])
        # Check non duplicate emails
        if emailCheck:
            errors['email'] = 'Email is already registered'
        # Password check
        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'
        # Role Checks
        if form['role'] == 'sysAdmin':
            if form['regcode'] not in regcodes:
                errors['regcode'] = 'Invalid Registration Code'
        if form['role'] == 'manager':
            if form['regcode'] not in codes:
                errors['regcode'] = 'Invalid Registration code'
        if form['role'] == 'employee':
            if form['email'] not in employees:
                errors['email'] = 'Please check with your employer'
        if form['role'] == 'owner':
            if form['regcode'] not in codes:
                errors['regcode'] = 'Invalid Registration code'
        return errors

    def updateEmail(self, form):
        errors = {}
        emailCheck = self.filter(email=form['email'])
        if emailCheck:
            errors['email'] = 'Email is already registered'
        return errors


# Log/Reg userData is id for Employee/Manager info
class User(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    level = models.IntegerField(default=0)
    loggedOn = models.DateTimeField(auto_now=True)
    userData = models.IntegerField(default=0)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    objects = UserManager()

# Created and maintained by user
class UserAddress(models.Model):
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=255)
    user = models.OneToOneField(User, unique=True, on_delete=CASCADE)

# Created and maintained by owner
class Company(models.Model):
    name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=255)
    owner = models.OneToOneField(User, unique=True, on_delete=CASCADE)

# Registration Codes added company in case user has app for multiple
class UserCodes(models.Model):
    userCode = models.CharField(max_length=255)
    lastUsed = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, related_name='companyCode', on_delete=CASCADE)
    creator = models.ForeignKey(User, related_name='codeCreator', on_delete=CASCADE)

# Allows for user to be a part of more than one company in app
class UserCompany(models.Model):
    theEmployee = models.ForeignKey(User, related_name='employeeOf', on_delete=CASCADE)
    theCompany = models.ForeignKey(Company, related_name='userCompany', on_delete=CASCADE)

# Department created and maintained by owner / manager
class Department(models.Model):
    name = models.CharField(max_length=255)
    toCompany = models.ForeignKey(Company,related_name='companyDepartment', on_delete=CASCADE)

#  payrates created and maintained by owner / manager
class PayRate(models.Model):
    rate = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    co = models.ForeignKey(Company,related_name='companyPay', on_delete=CASCADE)

# Employee information created and maintained by owner / manager
class Employee(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    payRate = models.ForeignKey(PayRate, related_name='employPay', on_delete=CASCADE)
    department = models.ForeignKey(Department, related_name='employDept', on_delete=CASCADE)
    hireDate = models.DateField()
    promotionDate = models.DateField(blank=True)
    lastPromotion = models.DateField(blank=True)
    terminationDate = models.DateField(blank=True)
    terminated = models.BooleanField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    workFor = models.ForeignKey(Company, related_name='workingFor', on_delete=CASCADE)

# Manager information created and maintained by owner / manager
class Management(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pay = models.ForeignKey(PayRate, related_name='managePay', on_delete=CASCADE)
    dept = models.ForeignKey(Department, related_name='manageDept', on_delete=CASCADE)
    hireDate = models.DateField()
    promotionDate = models.DateField(blank=True)
    lastPromotion = models.DateField(blank=True)
    terminationDate = models.DateField(blank=True)
    terminated = models.BooleanField(default=0)
    title = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    managerFor = models.ForeignKey(Company, related_name='managerOf', on_delete=CASCADE)

# Clock in / out part
class ClockInOut(models.Model):
    clockIn = models.DateTimeField(auto_now_add=True)
    clockOut = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(User, related_name='theEmployee', on_delete=CASCADE)