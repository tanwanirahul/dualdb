'''
Created on 07-Apr-2014

@author: Rahul
'''

from tastypie.resources import ModelResource
from tastypie.utils.mime import determine_format
from dualdb.core.models import Supplier, Customer, Product, Order
from tastypie.authorization import Authorization
from dualdb.common.utils import get_pk_filds


class BaseResource(ModelResource):
    '''
        Base of all the resources in our system.
        Framework modification and generally applicable
        changes will go here.
    '''
    class Meta(object):
        '''
            Meta options for all the resources.
        '''
        collection_name = "data"
        authorization = Authorization()

    def determine_format(self, request):
        '''
            Overriding text/html to application/json for ease of use through
            direct browser call.
        '''
        fmt = determine_format(request, self._meta.serializer,
                               default_format=self._meta.default_format)
        if fmt == 'text/html':
            fmt = 'application/json'

        return fmt


class SuppliersResource(BaseResource):
    '''
        Represents the API resource for Customer entity.
    '''
    class Meta(BaseResource.Meta):
        '''
            Holds META options for Suppliers resource.
            This resource has /suppliers/ end point URI.
        '''
        resource_name = "suppliers"
        queryset = Supplier.objects.all()
        excludes = get_pk_filds(Supplier)


class CustomersResource(BaseResource):
    '''
        Represents the API resource for Customer entity.
    '''
    class Meta(BaseResource.Meta):
        '''
            Holds META options for Customers resource.
            This resource has /customers/ end point URI.
        '''
        resource_name = "customers"
        queryset = Customer.objects.all()
        excludes = get_pk_filds(Customer)


class ProductsResource(BaseResource):
    '''
        Represents the API resource for Product entity.
    '''
    class Meta(BaseResource.Meta):
        '''
            Holds META options for Products resource.
            This resource has /products/ end point URI.
        '''
        resource_name = "products"
        queryset = Product.objects.all()
        excludes = get_pk_filds(Product)


class OrdersResource(BaseResource):
    '''
        Represents the API resource for Product entity.
    '''
    class Meta(BaseResource.Meta):
        '''
            Holds META options for Orders resource.
            This resource has /orders/ end point URI.
        '''
        resource_name = "orders"
        queryset = Order.objects.all()
        excludes = get_pk_filds(Order)
