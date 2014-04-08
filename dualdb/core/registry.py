'''
Created on 08-Apr-2014

@author: Rahul
'''
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
REGISTRY = {}


def register(db_name):
    '''
        A decorator generator to accept the DB name as parameter.
    '''
    if db_name not in settings.DATABASES:
        raise ImproperlyConfigured('''The {0} database, specified on model
        class ,does not have associated settings.'''.format(db_name))

    def class_wrapper(model_class):
        '''
            Registers the model class into registry to keep the mapping
            of model class and its associated database.
        '''
        REGISTRY.update({model_class: db_name})

        #Hack to maintain the registry of all ManyToMany fields of auth.
        for field in model_class._meta.local_many_to_many:
            REGISTRY.update({field.rel.through: db_name})

        return model_class

    return class_wrapper
