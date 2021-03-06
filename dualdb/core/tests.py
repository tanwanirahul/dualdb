'''
Created on 08-Apr-2014

@author: Rahul
'''
from tastypie.test import ResourceTestCase
from copy import deepcopy


class BaseClient(ResourceTestCase):
    '''
        This base class builds the basic infrastructure
        required to run the test cases.
    '''

    def get_full_uri(self, api_name, resource_name, *args, **kwargs):
        '''
            Joins all the pieces and returns the URI.
        '''
        bits = ['', api_name, resource_name]
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
        data = self.deserialize(resp)
        self._check_required_response_attributes(data)
        return data

    def get_xml_list(self, resource_name, api_name="v1"):
        '''
            Expects the valid XML data for list URI call on
            the given resource.
        '''
        resp = self.get_list(resource_name, api_name, accept_format="xml")
        self.assertHttpOK(resp)
        self.assertValidXMLResponse(resp)
        return True

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
               content_type="json"):
        '''
            Makes a POST call on the given resource to create a new instance
            and returns the resource id of the same.
        '''
        uri = self.get_full_uri(api_name, resource_name)
        resp = self.api_client.post(uri, format=content_type, data=data)
        self.assertHttpCreated(resp)
        return self._get_location_id(resp)

    def update(self, resource_name, object_id, data, api_name="v1",
               content_type="json"):
        '''
            Simulates a PUT call on the given resource to update the data.
        '''
        uri = self.get_full_uri(api_name, resource_name, object_id)
        resp = self.api_client.put(uri, format=content_type, data=data)
        self.assertHttpAccepted(resp)
        return True

    def delete(self, resource_name, object_id, api_name="v1"):
        '''
            Simulates a DELETE call on the given resource.
        '''
        uri = self.get_full_uri(api_name, resource_name, object_id)
        resp = self.api_client.delete(uri)
        self.assertHttpAccepted(resp)
        return True

    def assert_end_to_end_create_flow(self, resource_name, data):
        '''
            Simulates the end to end create flow.
            Get the initial count,
            Create a new instance,
            Assert total count in list URI,
            Make a detail URI and assert the same data is available.
        '''
        initial_count = self._get_list_uri_count(resource_name)
        res_id = self.create(resource_name, data)
        updated_count = self._get_list_uri_count(resource_name)
        self.assertEqual(initial_count + 1, updated_count,
                                "Count mismatch after creating new instance")
        res_data = self.get_json_detail(resource_name, object_id=res_id)
        self._assert_dict_matches(data, res_data)

    def assert_end_to_end_update_flow(self, resource_name, initial_data,
                                      updated_data):
        '''
            Simulates the end to end update flow.
            Update the first object loaded via fixtures to updated data
            and assert the data matches.
        '''

        # We get it from fixtures.
        res_id = "1"

        self.update(resource_name, object_id=res_id, data=updated_data)

        res_data = self.get_json_detail(resource_name, object_id=res_id)

        self._assert_dict_matches(updated_data, res_data)

    def assert_end_to_end_delete_flow(self, resource_name, data):
        '''
            Simulates the end to end delete flow.
            Get initial count.
            Get the data for first object loaded via fixtures through
            detail API call.
            Delete the same and make a GET call again, we should get back
            404 and total_count in LIST URI should be updated.
        '''

        initial_count = self._get_list_uri_count(resource_name)

        #We get it from loading of fixtures.
        res_id = "1"
        res_data = self.get_json_detail(resource_name, object_id=res_id)

        self.delete(resource_name, object_id=res_id)

        updated_count = self._get_list_uri_count(resource_name)

        self.assertEqual(initial_count - 1, updated_count,
                                "Count mismatch after deleting a new instance")

        self.assert_not_found_detail_uri(resource_name, object_id=res_id)

    def assert_not_found_detail_uri(self, resource_name, object_id,
                                api_name="v1", accept_format="json"):
        '''
            Makes a List URI call, and asserts that the response
            is not found.
        '''
        resp = self.get_detail(resource_name, object_id, api_name,
                               accept_format=accept_format)
        self.assertHttpNotFound(resp)

    def _get_list_uri_count(self, resource_name):
        '''
            Makes a LIST URI call for this resource and returns the total
            count.
        '''
        list_data = self.get_json_list(resource_name)
        total_count = list_data["meta"]["total_count"]
        return total_count

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
        location = self._get_location(resp)
        res_uri = '/%s' % ('/'.join(location[1].split("/")[3:]))
        return res_uri

    def _get_location_id(self, resp):
        '''Return resource_id for newly posted object
        '''
        location_uri = self._get_location_uri(resp)
        if location_uri.endswith("/"):
            location_uri = location_uri[:-1]
        res_id = location_uri.split('/')[-1]
        return res_id

    def _check_required_response_attributes(self, data):
        '''
            Given the response data, checks if data and meta attributes
            are present.
        '''
        self.assertIn("data", data, "Missing data attribute in List response")
        self.assertIn("meta", data, "Missing meta attribute in List response")

    def _assert_dict_matches(self, expected, under_test):
        '''
            Given expected and under_test dict, asserts if the former is subset
            of the later.
        '''
        for key, value in expected.items():
            self.assertEqual(under_test.get(key), value,
                             "Mismatch for key : {0}".format(key))


class CustomersTest(BaseClient):
    '''
        Tests basic REST API functionality for customers resource.
    '''
    multi_db = True
    fixtures = ["customers.json"]

    def setUp(self):
        '''
            Basic Pre-Requisite setup.
        '''
        super(CustomersTest, self).setUp()
        self.resource_name = "customers"
        self.data = {
                        "username": "customer1",
                        "first_name": "customer",
                        "password": "secret",
                        "last_name": "family_name",
                        "email": "customer@orders.com"
                     }

        self.update_data = {
                        "last_name": "surname"
                       }

    def test_get_json_list(self):
        '''
            Tests if the List URI with JSON data is working.
        '''
        self.get_json_list(self.resource_name)

    def test_get_xml_list(self):
        '''
            Tests if the List URI with JSON data is working.
        '''
        self.get_xml_list(self.resource_name)

    def test_create(self):
        '''
            Creates new instance of customers
            and makes a detail URI call on new id
            also assert total_count increased.
        '''
        self.assert_end_to_end_create_flow(self.resource_name, self.data)

    def test_update(self):
        '''
            Updates the first object loaded via fixtures;
            Asserts that the updated changes and reflected in detail call.
        '''
        updated_data = deepcopy(self.data)
        updated_data.update(self.update_data)
        self.assert_end_to_end_update_flow(self.resource_name,
                        initial_data=self.data, updated_data=updated_data)

    def test_delete(self):
        '''
            Makes sure it exists on detail URI call;
            Deletes the same;
            and checks the same has been deleted in LIST URI call.
        '''
        self.assert_end_to_end_delete_flow(self.resource_name, self.data)


class SuppliersTest(BaseClient):
    '''
        Tests basic REST API functionality for customers resource.
    '''
    multi_db = True
    fixtures = ["suppliers.json"]

    def setUp(self):
        '''
            Basic Pre-Requisite setup.
        '''
        super(SuppliersTest, self).setUp()
        self.resource_name = "suppliers"
        self.data = {
                        "username": "supplier1",
                        "first_name": "supplier",
                        "password": "secret",
                        "last_name": "family_name",
                        "email": "supplier@products.com"
                     }

        self.update_data = {
                        "last_name": "surname"
                       }

    def test_get_json_list(self):
        '''
            Tests if the List URI with JSON data is working.
        '''
        self.get_json_list(self.resource_name)

    def test_get_xml_list(self):
        '''
            Tests if the List URI with JSON data is working.
        '''
        self.get_xml_list(self.resource_name)

    def test_create(self):
        '''
            Creates new instance of customers
            and makes a detail URI call on new id
            also assert total_count increased.
        '''
        self.assert_end_to_end_create_flow(self.resource_name, self.data)

    def test_update(self):
        '''
            Updates the first object loaded via fixtures;
            Asserts that the updated changes and reflected in detail call.
        '''
        updated_data = deepcopy(self.data)
        updated_data.update(self.update_data)
        self.assert_end_to_end_update_flow(self.resource_name,
                        initial_data=self.data, updated_data=updated_data)

    def test_delete(self):
        '''
            Makes sure it exists on detail URI call;
            Deletes the same;
            and checks the same has been deleted in LIST URI call.
        '''
        self.assert_end_to_end_delete_flow(self.resource_name, self.data)


class OrdersTest(BaseClient):
    '''
        Tests basic REST API functionality for customers resource.
    '''
    multi_db = True
    fixtures = ["customers.json", "orders.json"]

    def setUp(self):
        '''
            Basic Pre-Requisite setup.
        '''
        super(OrdersTest, self).setUp()
        self.resource_name = "orders"
        self.data = {
                        "amount": 26.7,
                        "date": "2014-04-08",
                        "customer": "/v1/customers/1",
                     }

        self.update_data = {
                        "amount": 101.7
                       }

    def test_get_json_list(self):
        '''
            Tests if the List URI with JSON data is working.
        '''
        self.get_json_list(self.resource_name)

    def test_get_xml_list(self):
        '''
            Tests if the List URI with JSON data is working.
        '''
        self.get_xml_list(self.resource_name)

    def test_create(self):
        '''
            Creates new instance of customers
            and makes a detail URI call on new id
            also assert total_count increased.
        '''
        self.assert_end_to_end_create_flow(self.resource_name, self.data)

    def test_update(self):
        '''
            Updates the first object loaded via fixtures;
            Asserts that the updated changes and reflected in detail call.
        '''
        updated_data = deepcopy(self.data)
        updated_data.update(self.update_data)
        self.assert_end_to_end_update_flow(self.resource_name,
                        initial_data=self.data, updated_data=updated_data)

    def test_delete(self):
        '''
            Makes sure it exists on detail URI call;
            Deletes the same;
            and checks the same has been deleted in LIST URI call.
        '''
        self.assert_end_to_end_delete_flow(self.resource_name, self.data)


class ProductsTest(BaseClient):
    '''
        Tests basic REST API functionality for customers resource.
    '''
    multi_db = True
    fixtures = ["suppliers.json", "products.json"]

    def setUp(self):
        '''
            Basic Pre-Requisite setup.
        '''
        super(ProductsTest, self).setUp()
        self.resource_name = "products"
        self.data = {
                        "title": "product1",
                        "stock": 12,
                        "price": 19.0,
                        "suppliers": ["/v1/suppliers/1",
                                      "/v1/suppliers/2",
                                      ]
                     }

        self.update_data = {
                        "stock": 10
                       }

    def test_get_json_list(self):
        '''
            Tests if the List URI with JSON data is working.
        '''
        self.get_json_list(self.resource_name)

    def test_get_xml_list(self):
        '''
            Tests if the List URI with JSON data is working.
        '''
        self.get_xml_list(self.resource_name)

    def test_create(self):
        '''
            Creates new instance of customers
            and makes a detail URI call on new id
            also assert total_count increased.
        '''
        self.assert_end_to_end_create_flow(self.resource_name, self.data)

    def test_update(self):
        '''
            Updates the first object loaded via fixtures;
            Asserts that the updated changes and reflected in detail call.
        '''
        updated_data = deepcopy(self.data)
        updated_data.update(self.update_data)
        self.assert_end_to_end_update_flow(self.resource_name,
                        initial_data=self.data, updated_data=updated_data)

    def test_delete(self):
        '''
            Makes sure it exists on detail URI call;
            Deletes the same;
            and checks the same has been deleted in LIST URI call.
        '''
        self.assert_end_to_end_delete_flow(self.resource_name, self.data)
