'''
Created on 08-Apr-2014

@author: Rahul
'''
from dualdb.core.registry import REGISTRY


class ModelRouter(object):
    '''
        Router to navigate the queries to proper DB based
        on the register decorator.
    '''
    def db_for_read(self, model, **hints):
        '''
            Returns the database name to perform read queries on this model.
        '''
        return self._get_db(model)

    def db_for_write(self, model, **hints):
        '''
            Returns the database name to perform write queries on this model.
        '''
        return self._get_db(model)

    def allow_syncdb(self, db, model):
        '''
            Returns if the model needs to be synchronized for this db.
        '''
        print "This is called for model", model
        print "App label is ", model._meta.app_label
        if not db == "default":
            return db == self._get_db(model)
        return None

    def _get_db(self, model):
        '''
            Returns the associated DB name for this model by looking up into
            registry.
        '''
        return REGISTRY.get(model)
