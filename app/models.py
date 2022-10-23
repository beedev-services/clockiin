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
            employees.append(e.email)
        # Creating list of manager emails
        managers = []
        managerList = Management.objects.all().values()
        for m in managerList:
            managers.append(m.email)
        # Check non duplicate emails
        if emailCheck:
            errors['email'] = 'Email is already registered'
        # Password check
        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'
        # Role Checks
        if form['role'] == 'manager':
            if form['regcode'] not in regcodes:
                errors['regcode'] = 'Invalid Registration Code'
            if form['email'] not in managers:
                errors['email'] = 'Please check with you employer'
            else:
                errors['email'] = 'Please chose another selection'
        if form['role'] == 'employee':
            if form['email'] not in employees:
                errors['email'] = 'Please check with your employer'
        if form['role'] == 'sysAdmin':
            if form['regcode'] not in regcodes:
                errors['regcode'] = 'Invalid Registration code'
        return errors

    def updateEmail(self, form):
        errors = {}
        emailCheck = self.filter(email=form['email'])
        if emailCheck:
            errors['email'] = 'Email is already registered'
        return errors

class User(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    level = models.IntegerField(default=0)
    loggedOn = models.DateTimeField(auto_now=True)
    workFor = models.IntegerField(default=0)
    theData = models.IntegerField(default=0)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    objects = UserManager()

class UserAddress(models.Model):
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=255)
    user = models.OneToOneField(User, unique=True, on_delete=CASCADE)

class Company(models.Model):
    name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=255)
    owner = models.OneToOneField(User, unique=True, on_delete=CASCADE)

class Department(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company,related_name='companyDepartment', on_delete=CASCADE)

class PayRate(models.Model):
    rate = models.CharField(max_length=255)
    co = models.ForeignKey(Company,related_name='companyPay', on_delete=CASCADE)

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
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    theCompany = models.ForeignKey(Company, related_name='workingFor', on_delete=CASCADE)

class Management(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pay = models.ForeignKey(PayRate, related_name='managePay', on_delete=CASCADE)
    dept = models.ForeignKey(Department, related_name='manageDept', on_delete=CASCADE)
    hireDate = models.DateField()
    promotionDate = models.DateField(blank=True)
    lastPromotion = models.DateField(blank=True)
    title = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    theCo = models.ForeignKey(Company, related_name='managerOf', on_delete=CASCADE)

class ClockInOut(models.Model):
    clockIn = models.DateTimeField(auto_now_add=True)
    clockOut = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(User, related_name='theEmployee', on_delete=CASCADE)