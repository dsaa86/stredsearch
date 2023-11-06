import datetime
import os
import sys
import unittest
from lib2to3.pytree import convert
from re import M
from typing import Union
from unittest.mock import MagicMock, patch

import requests
from django.test import TestCase
from search.helperfunctions import *
from search.stackquery import *

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestStackQuery(TestCase):

    @patch('search.stackquery.checkObjAndRaiseTypeError')
    @patch('search.stackquery.checkStringAndRaiseValueError')
    @patch('search.stackquery.getRoutePrepend')
    @patch('search.stackquery.getAPIRoute')
    @patch('search.stackquery.getRouteAppend')
    @patch('requests.get')
    @patch ('search.stackquery.sanitiseStackOverflowResponse')
    def test_queryStackOverflow(self, mock_sanitiseStackOverflowResponse, mock_get, mock_getRouteAppend, mock_getAPIRoute, mock_getRoutePrepend, mock_checkStringAndRaiseValueError, mock_checkObjAndRaiseTypeError):
        # Set up the mocks
        mock_checkObjAndRaiseTypeError.return_value = True
        mock_checkStringAndRaiseValueError.return_value = True
        mock_getRoutePrepend.return_value = 'https://api.stackexchange.com'
        mock_getAPIRoute.return_value = '/2.3/questions'
        mock_getRouteAppend.return_value = 'stackoverflow'
        mock_sanitiseStackOverflowResponse.return_value = []
        mock_get.return_value = MagicMock(content='{"items": []}')

        # Call the function with test inputs
        response = queryStackOverflow('questions', 'question_by_tag', {'tagged': 'python'})

        # Assert that the mocks were called with the correct arguments
        mock_getRoutePrepend.assert_called_once()
        mock_getAPIRoute.assert_called_once_with('questions', 'question_by_tag')
        mock_getRouteAppend.assert_called_once()
        mock_get.assert_called_once_with('https://api.stackexchange.com/2.3/questions', {'tagged': 'python', 'site': 'stackoverflow'})
        mock_sanitiseStackOverflowResponse.assert_called_once_with({'items': []})

        # Assert that the function returned the expected result
        self.assertEqual(response, [])

        mock_checkObjAndRaiseTypeError.return_value = True
        mock_checkStringAndRaiseValueError.return_value = True
        mock_getRoutePrepend.return_value = 'https://api.stackexchange.com'
        mock_getAPIRoute.return_value = '/2.3/questions'
        mock_getRouteAppend.return_value = 'stackoverflow'
        mock_sanitiseStackOverflowResponse.return_value = []
        # mock_get.return_value = MagicMock(content='{"items": []}')
        mock_get.side_effect = requests.exceptions.SSLError('SSL Error')
        response = queryStackOverflow('questions', 'related_questions', {'ids': '123'})
        self.assertEqual(response, { "Error": { "SSLError": 'SSL Error' } })

    # @patch('search.stackquery.checkObjAndRaiseTypeError')
    # @patch('search.stackquery.checkStringAndRaiseValueError')
    # @patch('search.stackquery.getRoutePrepend')
    # @patch('search.stackquery.getAPIRoute')
    # @patch('search.stackquery.getRouteAppend')
    # @patch('requests.get')
    # @patch ('search.stackquery.sanitiseStackOverflowResponse')
    # def test_queryStackOverflow_raises_SSLError(self, mock_sanitiseStackOverflowResponse, mock_get, mock_getRouteAppend, mock_getAPIRoute, mock_getRoutePrepend, mock_checkStringAndRaiseValueError, mock_checkObjAndRaiseTypeError):
    #     mock_checkObjAndRaiseTypeError.return_value = True
    #     mock_checkStringAndRaiseValueError.return_value = True
    #     mock_getRoutePrepend.return_value = 'https://api.stackexchange.com'
    #     mock_getAPIRoute.return_value = '/2.3/questions'
    #     mock_getRouteAppend.return_value = 'stackoverflow'
    #     mock_sanitiseStackOverflowResponse.return_value = []
    #     # mock_get.return_value = MagicMock(content='{"items": []}')
    #     mock_get.side_effect = requests.exceptions.SSLError('SSL Error')
    #     response = queryStackOverflow('questions', 'related_questions', {'ids': '123'})
    #     self.assertEqual(response, { "Error": { "SSLError": 'SSL Error' } })

    
    @patch('search.stackquery.checkObjAndRaiseTypeError')
    @patch('search.stackquery.checkStringAndRaiseValueError')
    @patch('search.stackquery.getRoutePrepend')
    @patch('search.stackquery.getAPIRoute')
    @patch('search.stackquery.getRouteAppend')
    @patch('requests.get')
    @patch ('search.stackquery.sanitiseStackOverflowResponse')
    def test_queryStackOverflow_raises_Timeout_Error(self, mock_sanitiseStackOverflowResponse, mock_get, mock_getRouteAppend, mock_getAPIRoute, mock_getRoutePrepend, mock_checkStringAndRaiseValueError, mock_checkObjAndRaiseTypeError):
        mock_checkObjAndRaiseTypeError.return_value = True
        mock_checkStringAndRaiseValueError.return_value = True
        mock_getRoutePrepend.return_value = 'https://api.stackexchange.com'
        mock_getAPIRoute.return_value = '/2.3/questions'
        mock_getRouteAppend.return_value = 'stackoverflow'
        mock_sanitiseStackOverflowResponse.return_value = []
        # mock_get.return_value = MagicMock(content='{"items": []}')
        mock_get.side_effect = requests.exceptions.Timeout('Timeout Error')
        response = queryStackOverflow('questions', 'related_questions', {'ids': '123'})
        self.assertEqual(response, { "Error": { "Timeout": 'Timeout Error' } })
    
    @patch('search.stackquery.checkObjAndRaiseTypeError')
    @patch('search.stackquery.checkStringAndRaiseValueError')
    @patch('search.stackquery.getRoutePrepend')
    @patch('search.stackquery.getAPIRoute')
    @patch('search.stackquery.getRouteAppend')
    @patch('requests.get')
    @patch ('search.stackquery.sanitiseStackOverflowResponse')
    def test_queryStackOverflow_raises_Connection_Error(self, mock_sanitiseStackOverflowResponse, mock_get, mock_getRouteAppend, mock_getAPIRoute, mock_getRoutePrepend, mock_checkStringAndRaiseValueError, mock_checkObjAndRaiseTypeError):
        mock_checkObjAndRaiseTypeError.return_value = True
        mock_checkStringAndRaiseValueError.return_value = True
        mock_getRoutePrepend.return_value = 'https://api.stackexchange.com'
        mock_getAPIRoute.return_value = '/2.3/questions'
        mock_getRouteAppend.return_value = 'stackoverflow'
        mock_sanitiseStackOverflowResponse.return_value = []
        # mock_get.return_value = MagicMock(content='{"items": []}')
        mock_get.side_effect = requests.exceptions.ConnectionError('Connection Error')
        response = queryStackOverflow('questions', 'related_questions', {'ids': '123'})
        self.assertEqual(response, { "Error": { "ConnectionError": 'Connection Error' } })
    
    @patch('search.stackquery.checkObjAndRaiseTypeError')
    @patch('search.stackquery.checkStringAndRaiseValueError')
    @patch('search.stackquery.getRoutePrepend')
    @patch('search.stackquery.getAPIRoute')
    @patch('search.stackquery.getRouteAppend')
    @patch('requests.get')
    @patch ('search.stackquery.sanitiseStackOverflowResponse')
    def test_queryStackOverflow_raises_HTTPError(self, mock_sanitiseStackOverflowResponse, mock_get, mock_getRouteAppend, mock_getAPIRoute, mock_getRoutePrepend, mock_checkStringAndRaiseValueError, mock_checkObjAndRaiseTypeError):
        mock_checkObjAndRaiseTypeError.return_value = True
        mock_checkStringAndRaiseValueError.return_value = True
        mock_getRoutePrepend.return_value = 'https://api.stackexchange.com'
        mock_getAPIRoute.return_value = '/2.3/questions'
        mock_getRouteAppend.return_value = 'stackoverflow'
        mock_sanitiseStackOverflowResponse.return_value = []
        # mock_get.return_value = MagicMock(content='{"items": []}')
        mock_get.side_effect = requests.exceptions.HTTPError('HTTP Error')
        response = queryStackOverflow('questions', 'related_questions', {'ids': '123'})
        self.assertEqual(response, { "Error": { "HTTPError": 'HTTP Error' } })
    
    @patch('search.stackquery.checkObjAndRaiseTypeError')
    @patch('search.stackquery.checkStringAndRaiseValueError')
    @patch('search.stackquery.getRoutePrepend')
    @patch('search.stackquery.getAPIRoute')
    @patch('search.stackquery.getRouteAppend')
    @patch('requests.get')
    @patch ('search.stackquery.sanitiseStackOverflowResponse')
    def test_queryStackOverflow_raises_Too_Many_Redirects_Error(self, mock_sanitiseStackOverflowResponse, mock_get, mock_getRouteAppend, mock_getAPIRoute, mock_getRoutePrepend, mock_checkStringAndRaiseValueError, mock_checkObjAndRaiseTypeError):
        mock_checkObjAndRaiseTypeError.return_value = True
        mock_checkStringAndRaiseValueError.return_value = True
        mock_getRoutePrepend.return_value = 'https://api.stackexchange.com'
        mock_getAPIRoute.return_value = '/2.3/questions'
        mock_getRouteAppend.return_value = 'stackoverflow'
        mock_sanitiseStackOverflowResponse.return_value = []
        # mock_get.return_value = MagicMock(content='{"items": []}')
        mock_get.side_effect = requests.exceptions.TooManyRedirects('TooManyRedirects Error')
        response = queryStackOverflow('questions', 'related_questions', {'ids': '123'})
        self.assertEqual(response, { "Error": { "TooManyRedirects": 'TooManyRedirects Error' } })
    
    @patch('search.stackquery.checkObjAndRaiseTypeError')
    @patch('search.stackquery.checkStringAndRaiseValueError')
    @patch('search.stackquery.getRoutePrepend')
    @patch('search.stackquery.getAPIRoute')
    @patch('search.stackquery.getRouteAppend')
    @patch('requests.get')
    @patch ('search.stackquery.sanitiseStackOverflowResponse')
    def test_queryStackOverflow_raises_Request_Exception(self, mock_sanitiseStackOverflowResponse, mock_get, mock_getRouteAppend, mock_getAPIRoute, mock_getRoutePrepend, mock_checkStringAndRaiseValueError, mock_checkObjAndRaiseTypeError):
        mock_checkObjAndRaiseTypeError.return_value = True
        mock_checkStringAndRaiseValueError.return_value = True
        mock_getRoutePrepend.return_value = 'https://api.stackexchange.com'
        mock_getAPIRoute.return_value = '/2.3/questions'
        mock_getRouteAppend.return_value = 'stackoverflow'
        mock_sanitiseStackOverflowResponse.return_value = []
        # mock_get.return_value = MagicMock(content='{"items": []}')
        mock_get.side_effect = requests.exceptions.RequestException('Request Exception')
        response = queryStackOverflow('questions', 'related_questions', {'ids': '123'})
        self.assertEqual(response, { "Error": { "RequestException": 'Request Exception' } })

    def test_checkObjAndRaiseTypeError_with_correct_type(self):
        result = checkObjAndRaiseTypeError("test", str, "Error message")
        self.assertEqual(result, True)


    def test_checkObjAndRaiseTypeError_with_incorrect_type(self):
        with self.assertRaises(TypeError):
            checkObjAndRaiseTypeError("test", int, "Error message")


    def test_checkStringAndRaiseValueError_with_correct_value(self):
        result = checkStringAndRaiseValueError("test", " ", "Error message")
        self.assertEqual(result, True)


    def test_checkStringAndRaiseValueError_with_incorrect_value(self):
        with self.assertRaises(ValueError):
            checkStringAndRaiseValueError("test", "test", "Error message")

        
    def test_checkElemExistsInListOrDict_with_elem_in_list(self):
        result = checkElemExistsInListOrDict("test", ["test", "another"], "Error message")
        self.assertEqual(result, True)

    def test_checkElemExistsInListOrDict_with_elem_not_in_list(self):
        with self.assertRaises(ValueError):
            checkElemExistsInListOrDict("not_in_list", ["test", "another"], "Error message")

    def test_checkElemExistsInListOrDict_with_elem_in_dict(self):
        result = checkElemExistsInListOrDict("test", {"test": "value", "another": "value"}, "Error message")
        self.assertEqual(result, True)

    def test_checkElemExistsInListOrDict_with_elem_not_in_dict(self):
        with self.assertRaises(ValueError):
            checkElemExistsInListOrDict("not_in_dict", {"test": "value", "another": "value"}, "Error message")

    
    @patch('stackquery.StackRouteMeta.objects.get')
    def test_getRoutePrepend(self, mock_get):
        # Set up the mock
        mock_obj = MagicMock()
        mock_obj.route_prepend = 'https://api.stackexchange.com/2.3/'
        mock_get.return_value = mock_obj

        # Call the function
        result = getRoutePrepend()

        # Assert that the mock was called with the correct arguments
        mock_get.assert_called_once_with(pk=1)

        # Assert that the function returned the expected result
        self.assertEqual(result, 'https://api.stackexchange.com/2.3/')


    @patch('stackquery.StackRoute.objects.filter')
    def test_getAPIRoute(self, mock_filter):
        # Set up the mock
        mock_obj = MagicMock()
        mock_obj.route = 'questions'
        mock_filter.return_value.first.return_value = mock_obj

        # Call the function
        result = getAPIRoute('questions', 'related_questions')

        # Assert that the mock was called with the correct arguments
        mock_filter.assert_called_once_with(route_category='questions', route_query='related_questions')

        # Assert that the function returned the expected result
        self.assertEqual(result, 'questions')


    @patch('stackquery.StackRouteMeta.objects.get')
    def test_getRouteAppend(self, mock_get):
        # Set up the mock
        mock_obj = MagicMock()
        mock_obj.route_append = 'stackoverflow'
        mock_get.return_value = mock_obj

        # Call the function
        result = getRouteAppend()

        # Assert that the mock was called with the correct arguments
        mock_get.assert_called_once_with(pk=1)

        # Assert that the function returned the expected result
        self.assertEqual(result, 'stackoverflow')


    @patch('stackquery.StackRouteMeta.objects.get')
    def test_getRouteAppend(self, mock_get):
        # Set up the mock
        mock_obj = MagicMock()
        mock_obj.route_append = 'stackoverflow'
        mock_get.return_value = mock_obj

        # Call the function
        result = getRouteAppend()

        # Assert that the mock was called with the correct arguments
        mock_get.assert_called_once_with(pk=1)

        # Assert that the function returned the expected result
        self.assertEqual(result, 'stackoverflow')


    @patch('search.stackquery.getOnlyQuestionsFromStackOverflowResponse')
    @patch('search.stackquery.getQuestionData')
    def test_sanitiseStackOverflowResponse(self, mock_getQuestionData, mock_getOnlyQuestionsFromStackOverflowResponse):

        json_data = {
                'items': [
                    {"tags" : ['python'], 
                    "owner": {
                        'user_id' : 123456,
                        'display_name' : 'david'
                        }
                    }, 
                    {"tags" : ['python'],
                    "owner": {
                        'user_id' : 123456,
                        'display_name' : 'david'
                        }
                    }
                ]
            }

        # Set up the mocks
        mock_getOnlyQuestionsFromStackOverflowResponse.return_value = [{"tags" : ['python'], "owner": {'user_id' : 123456, 'display_name' : 'david'}}, {"tags" : ['python'], "owner": {'user_id' : 123456, 'display_name' : 'david'}}]

        mock_getQuestionData.side_effect = {
            'tags' : 'python',
            'user_id' : 123456,
            'display_name' : 'david',
        }

        # Call the function
        result = sanitiseStackOverflowResponse(json_data)

        # Assert that the mocks were called with the correct arguments
        mock_getOnlyQuestionsFromStackOverflowResponse.assert_called_once_with(json_data)
        mock_getQuestionData.assert_any_call({"tags" : ['python'], "owner": {'user_id' : 123456, 'display_name' : 'david'}})
        mock_getQuestionData.assert_any_call({"tags" : ['python'], "owner": {'user_id' : 123456, 'display_name' : 'david'}})

        # Assert that the function returned the expected result
        self.assertEqual(result, ['tags', 'user_id'])


    def test_getOnlyQuestionsFromStackOverflowResponse_valid_input(self):
        # Call the function with valid input
        result = getOnlyQuestionsFromStackOverflowResponse({'items': ['question1', 'question2']})

        # Assert that the function returned the expected result
        self.assertEqual(result, ['question1', 'question2'])

    def test_getOnlyQuestionsFromStackOverflowResponse_invalid_input_type(self):
        # Call the function with invalid input type and assert that it raises a TypeError
        with self.assertRaises(TypeError):
            getOnlyQuestionsFromStackOverflowResponse('invalid input type')

    def test_getOnlyQuestionsFromStackOverflowResponse_missing_items_key(self):
        # Call the function with missing 'items' key and assert that it raises a ValueError
        with self.assertRaises(ValueError):
            getOnlyQuestionsFromStackOverflowResponse({'invalid_key': 'value'})

    def test_getOnlyQuestionsFromStackOverflowResponse_empty_items_key(self):
        # Call the function with empty 'items' key and assert that it raises a ValueError
        with self.assertRaises(ValueError):
            getOnlyQuestionsFromStackOverflowResponse({'items': []})


    def test_getQuestionData_valid_input(self):
        # Call the function with valid input
        question = {
            "tags": ["python", "django"],
            "owner": {
                "user_id": 123456,
                "display_name": "test_user"
            }
        }
        result = getQuestionData(question)

        # Assert that the function returned the expected result
        expected_result = {
            "tags": "python, django",
            "user_id": 123456,
            "display_name": "test_user"
        }
        self.assertEqual(result, expected_result)

    def test_getQuestionData_invalid_input_type(self):
        # Call the function with invalid input type and assert that it raises a TypeError
        with self.assertRaises(TypeError):
            getQuestionData("invalid input type")

    def test_getQuestionData_missing_tags_key(self):
        # Call the function with missing 'tags' key and assert that it raises a ValueError
        question = {
            "owner": {
                "user_id": 123456,
                "display_name": "test_user"
            }
        }
        with self.assertRaises(ValueError):
            getQuestionData(question)

    def test_getQuestionData_missing_owner_key(self):
        # Call the function with missing 'owner' key and assert that it raises a ValueError
        question = {
            "tags": ["python", "django"]
        }
        with self.assertRaises(ValueError):
            getQuestionData(question)


    def test_extractOwnerData_valid_input(self):
        # Call the function with valid input
        question = {
            "owner": {
                "user_id": 123456,
                "display_name": "test_user"
            }
        }
        result_user_id = extractOwnerData(question, "user_id")
        result_display_name = extractOwnerData(question, "display_name")

        # Assert that the function returned the expected result
        self.assertEqual(result_user_id, 123456)
        self.assertEqual(result_display_name, "test_user")

    def test_extractOwnerData_invalid_input_type(self):
        # Call the function with invalid input type and assert that it raises a TypeError
        with self.assertRaises(TypeError):
            extractOwnerData("invalid input type", "user_id")

    def test_extractOwnerData_missing_owner_key(self):
        # Call the function with missing 'owner' key and assert that it raises a ValueError
        question = {
            "tags": ["python", "django"]
        }
        with self.assertRaises(ValueError):
            extractOwnerData(question, "user_id")

    def test_extractOwnerData_invalid_user_id_key(self):
        # Call the function with invalid 'user_id' key and assert that it raises an InvalidUserIdKey exception
        question = {
            "owner": {
                "display_name": "test_user"
            }
        }
        with self.assertRaises(InvalidUserIdKey):
            extractOwnerData(question, "user_id")

    def test_extractOwnerData_invalid_display_name_key(self):
        # Call the function with invalid 'display_name' key and assert that it raises an InvalidDisplayNameKey exception
        question = {
            "owner": {
                "user_id": 123456
            }
        }
        with self.assertRaises(InvalidDisplayNameKey):
            extractOwnerData(question, "display_name")


    @patch('search.stackquery.getQuestionDataFields')
    def test_extractRelevantQuestionDataFieldsForQuestion_valid_input(self, mock_getQuestionDataFields):
        # Set up the mock to return a specific result
        mock_getQuestionDataFields.return_value = ["title", "creation_date", "last_activity_date", "last_edit_date"]

        # Call the function with valid input
        question = {
            "title": "Test title",
            "creation_date": 1633048641,
            "last_activity_date": 1633048641,
            "last_edit_date": 1633048641,
            "other_field": "Not relevant"
        }
        result = extractRelevantQuestionDataFieldsForQuestion(question)

        # Assert that the function returned the expected result
        expected_result = {
            "title": "Test title",
            "creation_date": datetime(2021, 10, 1, 4, 37, 21),
            "last_activity_date": datetime(2021, 10, 1, 4, 37, 21),
            "last_edit_date": datetime(2021, 10, 1, 4, 37, 21)
        }
        self.assertEqual(result, expected_result)


    def test_extractRelevantQuestionDataFieldsForQuestion_invalid_input_type(self):
        # Call the function with invalid input type and assert that it raises a TypeError
        with self.assertRaises(TypeError):
            extractRelevantQuestionDataFieldsForQuestion("invalid input type")

    def test_extractRelevantQuestionDataFieldsForQuestion_missing_relevant_fields(self):
        # Call the function with missing relevant fields and assert that it returns an empty dictionary
        question = {
            "other_field": "Not relevant"
        }
        result = extractRelevantQuestionDataFieldsForQuestion(question)
        self.assertEqual(result, {})

    @patch('search.stackquery.getQuestionDataFields')
    def test_extractRelevantQuestionDataFieldsForQuestion_invalid_timestamp(self, mock_getQuestionDataFields):

        mock_getQuestionDataFields.return_value = ["title", "creation_date", "last_activity_date", "last_edit_date"]
        # Call the function with invalid timestamp and assert that it returns an error dictionary
        question = {
            "creation_date": "invalid timestamp"
        }
        result = extractRelevantQuestionDataFieldsForQuestion(question)
        self.assertEqual(result, {'error': {'TypeError': 'ms_value must be of type int'}})


    @patch('stackquery.StackQuestionDataFields.objects.all')
    def test_getQuestionDataFields(self, mock_objects_all):
        # Set up the mock to return a specific result
        mock_objects_all.return_value = [
            MagicMock(data_field_name='title'),
            MagicMock(data_field_name='creation_date'),
            MagicMock(data_field_name='last_activity_date'),
            MagicMock(data_field_name='last_edit_date'),
        ]

        # Call the function
        result = getQuestionDataFields()

        # Assert that the function returned the expected result
        expected_result = ['title', 'creation_date', 'last_activity_date', 'last_edit_date']
        self.assertEqual(result, expected_result)