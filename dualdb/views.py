'''
Created on 08-Apr-2014

@author: Rahul
'''
from django.http.response import HttpResponse
from dualdb.core.models import Product


def hello(request):
    '''
        This is just to test
    '''
    print dir(Product.pk)
    return HttpResponse("This is working")
