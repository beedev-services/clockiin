from django.db import models
from django.core.validators import RegexValidator
import re
from django.db.models.fields import BooleanField, CharField
from django.db.models.signals import post_save
from django.db.models.deletion import CASCADE
import datetime
from .regcodes import *

class UserManager(models.Manager):
    def validate(self, form):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        emailCheck = self.filter(email=form['email'])
        if emailCheck:
            errors['email'] = 'Email is already registered'
        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'
        if form['role'] == 'Employer':
            if form['REGCODE'] not in regcodes:
                errors['REGCODE'] = 'Invalid Registration Code'
            else:
                managerList = Management.objects.all().values()
                managers = []
                for manager in managerList:
                    managers.append(manager.email)
                return managers
                if form['email'] not in managers:
                    errors['email'] = 'Please reach out to your employer to gain access or chose employee'
        if form['role'] == 'Employee':
            employeeList = Employee.objects.all().values()
            emailList = []
            for employee in employeeList:
                emailList.append(employee.email)
            return emailList
            if form['email'] not in emailList:
                errors['email'] = 'Please reach out to your employer to be added to database'
                
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
    username = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=255)
    level = models.IntegerField(default=0)
    employer = models.IntegerField(default=0)

    objects = UserManager()

    loggedOn = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

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
    company = models.ForeignKey(Company,related_name='companyPay', on_delete=CASCADE)


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
    company = models.ForeignKey(Company, related_name='workingFor', on_delete=CASCADE)

class Management(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    payRate = models.ForeignKey(PayRate, related_name='employPay', on_delete=CASCADE)
    department = models.ForeignKey(Department, related_name='employDept', on_delete=CASCADE)
    hireDate = models.DateField()
    promotionDate = models.DateField(blank=True)
    lastPromotion = models.DateField(blank=True)
    title = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, related_name='managerOf', on_delete=CASCADE)

class ClockInOut(models.Model):
    clockIn = models.DateTimeField(auto_now_add=True)
    clockOut = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(User, related_name='theEmployee', on_delete=CASCADE)