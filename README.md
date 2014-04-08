dualdb
======

##How to Get Started?

1. Craete a new virtual environment for dependencies management.
2. Install dependencies specified in requirements.txt. 
3. Syncdb. (We should rather use south).
*    python manage.py syncdb
*    python manage.py syncdb --database inventory
*    python manage.py syncdb --database transactions
4. Run tests. Python manage.py test core

##How to explore?

Run the development server and point your browser to v1 version of our APIs. /v1/. This should list all the available service end=points.

Currently we have:

* /v1/customers
* /v1/orders
* /v1/suppliers
* /v1/products

First two needs inventory database for their storage requirements while later two are being mapped to inventory.

Currently all the services support most of the basic HTTP verbs (GET, POST, PUT, DELETE, PATCH etc) without any authentication / authorization.
