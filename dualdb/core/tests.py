'''
Created on 08-Apr-2014

@author: Rahul
'''
from tastypie.test import ResourceTestCase
import json


class BaseClient(ResourceTestCase):
    '''
        This base class builds the basic infrastructure
        required to run the test cases.
    '''
    
    def get_full_uri(self, api_name, resource_name, *args, **kwargs):
        '''
            Joins all the pieces and returns the URI.
        '''
        bits = [api_name, resource_name]
        bits.extend(args)
        return '/'.join(bits)

    def get_list(self, resource_name, api_name="v1", accept_format="json"):
        '''
            Returns the result of list URI call on a resource.
        '''
        uri = self.get_full_uri(api_name, resource_name)
        resp = self.api_client.get(uri, format=accept_format)
        return resp

    def get_json_list(self, resource_name, api_name="v1"):
        '''
            Expects the valid JSON data for list URI call on
            the given resource.
        '''
        resp = self.get_list(resource_name, api_name, accept_format="json")
        self.assertHttpOK(resp)
        self.assertValidJSONResponse(resp)
        return self.deserialize(resp)

    def get_xml_list(self, resource_name, api_name="v1"):
        '''
            Expects the valid XML data for list URI call on
            the given resource.
        '''
        resp = self.get_list(resource_name, api_name, accept_format="xml")
        self.assertHttpOK(resp)
        self.assertValidJSONResponse(resp)
        return self.deserialize(resp)

    def get_detail(self, resource_name, object_id, api_name, accept_format):
        '''
            Given the resource name and object id, makes a PUT call
            on detail URI to update the data.
        '''
        uri = self.get_full_uri(api_name, resource_name, object_id)
        resp = self.api_client.get(uri, format=accept_format)
        return resp

    def get_json_detail(self, resource_name, object_id, api_name="v1"):
        '''
            Expects the valid JSON data for detail URI call on
            the given resource.
        '''
        resp = self.get_detail(resource_name, object_id, api_name,
                               accept_format="json")
        self.assertHttpOK(resp)
        self.assertValidJSONResponse(resp)
        return self.deserialize(resp)

    def get_xml_detail(self, resource_name, object_id, api_name="v1"):
        '''
            Expects the valid JSON data for detail URI call on
            the given resource.
        '''
        resp = self.get_detail(resource_name, object_id, api_name,
                               accept_format="xml")
        self.assertHttpOK(resp)
        self.assertValidXMLResponse(resp)
        return self.deserialize(resp)

    def create(self, resource_name, data, api_name="v1",
               content_type="application/json"):
        '''
            Makes a POST call on the given resource to create a new instance
            and returns the resource id of the same.
        '''
        uri = self.get_full_uri(api_name, resource_name)
        resp = self.api_client.post(uri, format=content_type, data=data)
        self.assertHttpCreated(resp)
        return self._get_location_id(resp)

    def update(self, resource_name, object_id, data, api_name="v1",
               content_type="application/json"):
        '''
            Simulates a PUT call on the given resource to update the data.
        '''
        uri = self.get_full_uri(api_name, resource_name, object_id)
        resp = self.api_client.put(uri, format=content_type, data=data)
        self.assertHttpAccepted(resp)
        return True

    def _get_location(self, resp):
        '''
            Returns the value of location header.
        '''
        headers = resp._headers
        location = headers.get("location", ("location", ""))
        return location

    def _get_location_uri(self, resp):
        '''
            Returns the resource uri for newly posted object.
        '''
        location = self.get_location(resp)
        res_uri = '/%s' % ('/'.join(location[1].split("/")[3:]))
        return res_uri

    def _get_location_id(self, resp):
        '''Return resource_id for newly posted object
        '''
        location_uri = self.get_location_uri(resp)
        if location_uri.endswith("/"):
            location_uri = location_uri[:-1]
        res_id = location_uri.split('/')[-1]
        return res_id
