from django.conf.urls import patterns, include, url
from dualdb.core.resources import CustomersResource, OrdersResource,\
    SuppliersResource, ProductsResource
from tastypie.api import Api

# Initializing the version V1 APIs.
V1_API = Api(api_name="v1")

V1_API.register(CustomersResource())
V1_API.register(OrdersResource())

V1_API.register(SuppliersResource())
V1_API.register(ProductsResource())

urlpatterns = patterns('',

    url(r'^$', 'dualdb.views.hello', name='hello'),
    (r'', include(V1_API.urls)),
)
