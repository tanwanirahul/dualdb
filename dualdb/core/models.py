'''
Created on 07-Apr-2014

@author: Rahul
'''

from django.db import models
from django.contrib import auth
from .registry import register

APP_LABEL = "core"


class User(auth.models.AbstractUser):
    '''
        Represent the User entity.
    '''
    #Assume we will get the S3(or any Public) URI for the same.
    avatar = models.CharField(max_length=300, null=True)

    class Meta(object):
        abstract = True


@register("inventory")
class Supplier(User):
    '''
        Represents the supplier entity.
    '''
    class Meta(object):
        app_label = APP_LABEL


@register("transactions")
class Customer(User):
    '''
        Represents our Customer entity.
    '''
    class Meta(object):
        app_label = APP_LABEL


@register("inventory")
class Product(models.Model):
    '''
        Represents our Product entity.
    '''
    title = models.CharField(max_length=30)
    price = models.FloatField()
    stock = models.IntegerField()
    suppliers = models.ManyToManyField(Supplier)

    class Meta(object):
        app_label = APP_LABEL


@register("transactions")
class Order(models.Model):
    '''
        Captures an instance of Order generation.
    '''
    amount = models.FloatField()
    date = models.DateField()
    customer = models.ForeignKey(Customer)

    class Meta(object):
        app_label = APP_LABEL
