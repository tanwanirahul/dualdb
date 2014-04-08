'''
Created on 08-Apr-2014

@author: Rahul
'''


def get_pk_filds(model_class):
    '''
        Given the model class, returns the list of primary key fields.
    '''
    return [field.name for field in model_class._meta.fields if\
                        field.primary_key]
