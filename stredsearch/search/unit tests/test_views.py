import os
import sys
from datetime import datetime
from unittest import mock
from unittest.mock import Mock, patch
from urllib.parse import quote

from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase
from search.models import (StackFilters, StackOrderMethods, StackParams,
                           StackQuestion, StackQuestionDataFields, StackRoute,
                           StackSortMethods, StackTags, StackUser)
from search.serializers import (RedditSearchQuerySerializer,
                                StackFiltersSerializer,
                                StackOrderMethodsSerializer,
                                StackParamsSerializer,
                                StackQuestionDataFieldsSerializer,
                                StackRouteSerializer,
                                StackSortMethodsSerializer,
                                StackTagsSerializer)
from search.views import (GetStackOverflowAdvancedSearch,
                          GetStackOverflowQuestionsByTag,
                          GetStackOverflowRelatedQuestions,
                          GetStackOverflowSimpleSearch)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class GetStackOverflowQuestionsByTagTest(APITestCase):
    def setUp(self):
        user = StackUser.objects.create(user_id=1, display_name="Test User")
        tag = StackTags.objects.create(tag_name="Test Tag", number_of_instances_on_so=10, number_of_cached_instances=5)
        self.question = StackQuestion.objects.create(
            owner=user,
            is_answered=False,
            view_count=100,
            answer_count=5,
            score=10,
            last_activity_date=datetime.now(),
            creation_date=datetime.now(),
            question_id=1
        )
        self.question.tags.add(tag)
        self.factory = APIRequestFactory()

    @patch('search.views.queryStackOverflow')
    @patch('search.views.insertStackQuestionsToDB')
    @patch('rq.Queue.enqueue')
    def test_get(self, mock_enqueue, mock_insertStackQuestionsToDB, mock_queryStackOverflow):
        mock_queryStackOverflow.return_value = [self.question]
        mock_insertStackQuestionsToDB.return_value = None
        mock_enqueue.return_value = None

        request = self.factory.get(reverse('GetStackOverflowQuestionsByTag', kwargs={
            'page': "1",
            'pagesize': "10",
            'fromdate': '2022-01-01',
            'todate': '2022-12-31',
            'order': 'desc',
            'sort': 'activity',
            'tags': 'python',
        }))
        response = GetStackOverflowQuestionsByTag.as_view()(request, page="1", pagesize="10", fromdate='2022-01-01', todate='2022-12-31', order='desc', sort='activity', tags='python')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['question_id'], 1)

    @patch('search.views.queryStackOverflow')
    @patch('search.views.insertStackQuestionsToDB')
    @patch('rq.Queue.enqueue')
    def test_get_error_handling(self, mock_enqueue, mock_insertStackQuestionsToDB, mock_queryStackOverflow):
        mock_queryStackOverflow.return_value = {"error": "Test error"}
        mock_insertStackQuestionsToDB.return_value = None
        mock_enqueue.return_value = None

        request = self.factory.get(reverse('GetStackOverflowQuestionsByTag', kwargs={
            'page': "1",
            'pagesize': "10",
            'fromdate': '2022-01-01',
            'todate': '2022-12-31',
            'order': 'desc',
            'sort': 'activity',
            'tags': 'python',
        }))
        response = GetStackOverflowQuestionsByTag.as_view()(request, page="1", pagesize="10", fromdate='2022-01-01', todate='2022-12-31', order='desc', sort='activity', tags='python')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['error'], "Test error")

    def test_get_invalid_parameters(self):
        request = self.factory.get(reverse('GetStackOverflowQuestionsByTag', kwargs={
            'page': 'invalid',
            'pagesize': 'invalid',
            'fromdate': 'invalid',
            'todate': 'invalid',
            'order': 'invalid',
            'sort': 'invalid',
            'tags': 'invalid',
        }))
        response = GetStackOverflowQuestionsByTag.as_view()(request, page='invalid', pagesize='invalid', fromdate='invalid', todate='invalid', order='invalid', sort='invalid', tags='invalid')

        self.assertEqual(response.status_code, 404)

    @patch('search.views.queryStackOverflow')
    @patch('search.views.insertStackQuestionsToDB')
    @patch('rq.Queue.enqueue')
    def test_get_edge_cases(self, mock_enqueue, mock_insertStackQuestionsToDB, mock_queryStackOverflow):
        mock_queryStackOverflow.return_value = []
        mock_insertStackQuestionsToDB.return_value = None
        mock_enqueue.return_value = None

        request = self.factory.get(reverse('GetStackOverflowQuestionsByTag', kwargs={
            'page': "1",
            'pagesize': "0",
            'fromdate': '2022-01-01',
            'todate': '2022-12-31',
            'order': 'desc',
            'sort': 'activity',
            'tags': 'python',
        }))
        response = GetStackOverflowQuestionsByTag.as_view()(request, page="1", pagesize="0", fromdate='2022-01-01', todate='2022-12-31', order='desc', sort='activity', tags='python')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    @patch('search.views.queryStackOverflow')
    @patch('search.views.insertStackQuestionsToDB')
    @patch('rq.Queue.enqueue')
    def test_get_performance(self, mock_enqueue, mock_insertStackQuestionsToDB, mock_queryStackOverflow):
        mock_queryStackOverflow.return_value = [self.question] * 1000
        mock_insertStackQuestionsToDB.return_value = None
        mock_enqueue.return_value = None

        request = self.factory.get(reverse('GetStackOverflowQuestionsByTag', kwargs={
            'page': "1",
            'pagesize': "1000",
            'fromdate': '2022-01-01',
            'todate': '2022-12-31',
            'order': 'desc',
            'sort': 'activity',
            'tags': 'python',
        }))
        response = GetStackOverflowQuestionsByTag.as_view()(request, page="1", pagesize="1000", fromdate='2022-01-01', todate='2022-12-31', order='desc', sort='activity', tags='python')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1000)


class GetStackOverflowRelatedQuestionsTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    @patch('search.views.queryStackOverflow')
    @patch('search.views.insertStackQuestionsToDB')
    @patch('rq.Queue.enqueue')
    def test_get_valid_parameters(self, mock_enqueue, mock_insertStackQuestionsToDB, mock_queryStackOverflow):
        mock_queryStackOverflow.return_value = [{
            'tags': 'python,django',
            'is_answered': True,
            'view_count': 100,
            'answer_count': 2,
            'score': 10,
            'last_activity_date': '2022-01-01T00:00:00Z',
            'creation_date': '2022-01-01T00:00:00Z',
            'last_edit_date': '2022-01-01T00:00:00Z',
            'question_id': 1,
            'link': 'https://stackoverflow.com/questions/1',
            'title': 'Test question',
            'user_id': 1,
            'display_name': 'Test user'
        }]
        mock_insertStackQuestionsToDB.return_value = None
        mock_enqueue.return_value = None

        request = self.factory.get(reverse('GetStackOverflowRelatedQuestions', kwargs={
            'page': "1",
            'pagesize': "10",
            'fromdate': '2022-01-01',
            'todate': '2022-12-31',
            'order': 'desc',
            'sort': 'activity',
            'ids': '1',
        }))
        response = GetStackOverflowRelatedQuestions.as_view()(request, page="1", pagesize="10", fromdate='2022-01-01', todate='2022-12-31', order='desc', sort='activity', ids='1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['question_id'], 1)

    @patch('search.views.queryStackOverflow')
    @patch('search.views.insertStackQuestionsToDB')
    @patch('rq.Queue.enqueue')
    def test_get_invalid_parameters(self, mock_enqueue, mock_insertStackQuestionsToDB, mock_queryStackOverflow):
        request = self.factory.get(reverse('GetStackOverflowRelatedQuestions', kwargs={
            'page': 'invalid',
            'pagesize': 'invalid',
            'fromdate': 'invalid',
            'todate': 'invalid',
            'order': 'invalid',
            'sort': 'invalid',
            'ids': 'invalid',
        }))
        response = GetStackOverflowRelatedQuestions.as_view()(request, page='invalid', pagesize='invalid', fromdate='invalid', todate='invalid', order='invalid', sort='invalid', ids='invalid')

        self.assertEqual(response.status_code, 404)

    @patch('search.views.queryStackOverflow')
    @patch('search.views.insertStackQuestionsToDB')
    @patch('rq.Queue.enqueue')
    def test_get_api_error(self, mock_enqueue, mock_insertStackQuestionsToDB, mock_queryStackOverflow):
        mock_queryStackOverflow.return_value = {'error': 'API error'}
        mock_insertStackQuestionsToDB.return_value = None
        mock_enqueue.return_value = None

        request = self.factory.get(reverse('GetStackOverflowRelatedQuestions', kwargs={
            'page': "1",
            'pagesize': "10",
            'fromdate': '2022-01-01',
            'todate': '2022-12-31',
            'order': 'desc',
            'sort': 'activity',
            'ids': '1',
        }))
        response = GetStackOverflowRelatedQuestions.as_view()(request, page="1", pagesize="10", fromdate='2022-01-01', todate='2022-12-31', order='desc', sort='activity', ids='1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['error'], 'API error')



class GetStackOverflowSimpleSearchTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    @patch('search.views.queryStackOverflow')
    @patch('search.views.insertStackQuestionsToDB')
    @patch('rq.Queue.enqueue')
    def test_get_valid_parameters(self, mock_enqueue, mock_insertStackQuestionsToDB, mock_queryStackOverflow):
        mock_queryStackOverflow.return_value = [{
            'tags': 'python,django',
            'is_answered': True,
            'view_count': 100,
            'answer_count': 2,
            'score': 10,
            'last_activity_date': '2022-01-01T00:00:00Z',
            'creation_date': '2022-01-01T00:00:00Z',
            'last_edit_date': '2022-01-01T00:00:00Z',
            'question_id': 1,
            'link': 'https://stackoverflow.com/questions/1',
            'title': 'Test question',
            'user_id': 1,
            'display_name': 'Test user'
        }]
        mock_insertStackQuestionsToDB.return_value = None
        mock_enqueue.return_value = None

        request = self.factory.get(reverse('GetStackOverflowSimpleSearch', kwargs={
            'page': "1",
            'pagesize': "10",
            'fromdate': '2022-01-01',
            'todate': '2022-12-31',
            'order': 'desc',
            'sort': 'activity',
            'nottagged': 'java',
            'tagged': 'python',
            'intitle': 'test',
        }))
        response = GetStackOverflowSimpleSearch.as_view()(request, page="1", pagesize="10", fromdate='2022-01-01', todate='2022-12-31', order='desc', sort='activity', nottagged='java', tagged='python', intitle='test')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['question_id'], 1)

    @patch('search.views.queryStackOverflow')
    @patch('search.views.insertStackQuestionsToDB')
    @patch('rq.Queue.enqueue')
    def test_get_invalid_parameters(self, mock_enqueue, mock_insertStackQuestionsToDB, mock_queryStackOverflow):
        request = self.factory.get(reverse('GetStackOverflowSimpleSearch', kwargs={
            'page': 'invalid',
            'pagesize': 'invalid',
            'fromdate': 'invalid',
            'todate': 'invalid',
            'order': 'invalid',
            'sort': 'invalid',
            'nottagged': 'invalid',
            'tagged': 'invalid',
            'intitle': 'invalid',
        }))
        response = GetStackOverflowSimpleSearch.as_view()(request, page='invalid', pagesize='invalid', fromdate='invalid', todate='invalid', order='invalid', sort='invalid', nottagged='invalid', tagged='invalid', intitle='invalid')

        self.assertEqual(response.status_code, 404)

    @patch('search.views.queryStackOverflow')
    @patch('search.views.insertStackQuestionsToDB')
    @patch('rq.Queue.enqueue')
    def test_get_api_error(self, mock_enqueue, mock_insertStackQuestionsToDB, mock_queryStackOverflow):
        # Mock the queryStackOverflow function to return an error
        mock_queryStackOverflow.return_value = {'error': 'API error'}
        mock_insertStackQuestionsToDB.return_value = None
        mock_enqueue.return_value = None

        request = self.factory.get(reverse('GetStackOverflowSimpleSearch', kwargs={
            'page': "1",
            'pagesize': "10",
            'fromdate': '2022-01-01',
            'todate': '2022-12-31',
            'order': 'desc',
            'sort': 'activity',
            'nottagged': 'java',
            'tagged': 'python',
            'intitle': 'test',
        }))
        response = GetStackOverflowSimpleSearch.as_view()(request, page="1", pagesize="10", fromdate='2022-01-01', todate='2022-12-31', order='desc', sort='activity', nottagged='java', tagged='python', intitle='test')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['error'], 'API error')


class GetStackOverflowAdvancedSearchTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    @patch('search.views.queryStackOverflow')
    @patch('search.views.insertStackQuestionsToDB')
    @patch('rq.Queue.enqueue')
    def test_get_valid_parameters(self, mock_enqueue, mock_insertStackQuestionsToDB, mock_queryStackOverflow):
        mock_queryStackOverflow.return_value = [{
            'tags': 'python,django',
            'is_answered': True,
            'view_count': 100,
            'answer_count': 2,
            'score': 10,
            'last_activity_date': '2022-01-01T00:00:00Z',
            'creation_date': '2022-01-01T00:00:00Z',
            'last_edit_date': '2022-01-01T00:00:00Z',
            'question_id': 1,
            'link': quote('https://stackoverflow.com/questions/1', safe=''),
            'title': 'Test question',
            'user_id': 1,
            'display_name': 'Test user'
        }]
        mock_insertStackQuestionsToDB.return_value = None
        mock_enqueue.return_value = None

        request = self.factory.get(reverse('GetStackOverflowAdvancedSearch', kwargs={
            'page': "1",
            'pagesize': "10",
            'fromdate': '2022-01-01',
            'todate': '2022-12-31',
            'order': 'desc',
            'sort': 'activity',
            'q': 'test',
            'accepted': 'True',
            'answers': '2',
            'body': 'test',
            'closed': 'False',
            'migrated': 'False',
            'notice': 'False',
            'nottagged': 'java',
            'tagged': 'python',
            'title': 'test',
            'user': '1',
            'url': quote('https://stackoverflow.com/questions/1', safe=''),
            'views': '100',
            'wiki': 'False',
        }))
        response = GetStackOverflowAdvancedSearch.as_view()(request, page="1", pagesize="10", fromdate='2022-01-01', todate='2022-12-31', order='desc', sort='activity', q='test', accepted='True', answers='2', body='test', closed='False', migrated='False', notice='False', nottagged='java', tagged='python', title='test', user='1', url='https://stackoverflow.com/questions/1', views='100', wiki='False')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['question_id'], 1)

    @patch('search.views.queryStackOverflow')
    @patch('search.views.insertStackQuestionsToDB')
    @patch('rq.Queue.enqueue')
    def test_get_invalid_parameters(self, mock_enqueue, mock_insertStackQuestionsToDB, mock_queryStackOverflow):
        request = self.factory.get(reverse('GetStackOverflowAdvancedSearch', kwargs={
            'page': 'invalid',
            'pagesize': 'invalid',
            'fromdate': 'invalid',
            'todate': 'invalid',
            'order': 'invalid',
            'sort': 'invalid',
            'q': 'invalid',
            'accepted': 'invalid',
            'answers': 'invalid',
            'body': 'invalid',
            'closed': 'invalid',
            'migrated': 'invalid',
            'notice': 'invalid',
            'nottagged': 'invalid',
            'tagged': 'invalid',
            'title': 'invalid',
            'user': 'invalid',
            'url': 'invalid',
            'views': 'invalid',
            'wiki': 'invalid',
        }))
        response = GetStackOverflowAdvancedSearch.as_view()(request, page='invalid', pagesize='invalid', fromdate='invalid', todate='invalid', order='invalid', sort='invalid', q='invalid', accepted='invalid', answers='invalid', body='invalid', closed='invalid', migrated='invalid', notice='invalid', nottagged='invalid', tagged='invalid', title='invalid', user='invalid', url='invalid', views='invalid', wiki='invalid')

        self.assertEqual(response.status_code, 404)

    @patch('search.views.queryStackOverflow')
    @patch('search.views.insertStackQuestionsToDB')
    @patch('rq.Queue.enqueue')
    def test_get_api_error(self, mock_enqueue, mock_insertStackQuestionsToDB, mock_queryStackOverflow):
        mock_queryStackOverflow.return_value = {'error': 'API error'}
        mock_insertStackQuestionsToDB.return_value = None
        mock_enqueue.return_value = None

        request = self.factory.get(reverse('GetStackOverflowAdvancedSearch', kwargs={
            'page': "1",
            'pagesize': "10",
            'fromdate': '2022-01-01',
            'todate': '2022-12-31',
            'order': 'desc',
            'sort': 'activity',
            'q': 'test',
            'accepted': 'True',
            'answers': '2',
            'body': 'test',
            'closed': 'False',
            'migrated': 'False',
            'notice': 'False',
            'nottagged': 'java',
            'tagged': 'python',
            'title': 'test',
            'user': '1',
            'url': quote('https://stackoverflow.com/questions/1', safe=''),
            'views': '100',
            'wiki': 'False',
        }))
        response = GetStackOverflowAdvancedSearch.as_view()(request, page="1", pagesize="10", fromdate='2022-01-01', todate='2022-12-31', order='desc', sort='activity', q='test', accepted='True', answers='2', body='test', closed='False', migrated='False', notice='False', nottagged='java', tagged='python', title='test', user='1', url='https://stackoverflow.com/questions/1', views='100', wiki='False')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['error'], 'API error')


class GetStackOverflowAllTagsInDBTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create some sample tags
        StackTags.objects.create(tag_name='python')
        StackTags.objects.create(tag_name='django')

    def test_get_all_tags(self):
        url = reverse('GetStackOverflowAllTagsInDB')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['tag_name'], 'python')
        self.assertEqual(response.data[1]['tag_name'], 'django')


class GetStackOverflowTagsFromSiteTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    @mock.patch('search.views.getTagsFromSO')
    @mock.patch('search.views.insertStackTagsToDB')
    @mock.patch('django_rq.get_queue')
    def test_get_tags_from_site(self, mock_get_queue, mock_insert_tags, mock_get_tags):
        mock_tags = [StackTags(tag_name='python'), StackTags(tag_name='django')]
        mock_get_tags.return_value = mock_tags

        mock_queue = mock.Mock()
        mock_get_queue.return_value = mock_queue

        url = reverse('GetStackOverflowTagsFromSite', kwargs={'pages': 1})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        mock_get_tags.assert_called_once_with(1)

        mock_get_queue.assert_called_once_with("default", autocommit=True, is_async=True)

        mock_queue.enqueue.assert_called_once_with(mock_insert_tags, mock_tags)

        expected_data = StackTagsSerializer(mock_tags, many=True).data
        self.assertEqual(response.data, expected_data)


class GetAllStackOverflowParamsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        StackParams.objects.create(param_name='param1', param_description='value1')
        StackParams.objects.create(param_name='param2', param_description='value2')

    def test_get_all_params(self):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['param_name'], 'param1')
        self.assertEqual(response.data[0]['param_description'], 'value1')
        self.assertEqual(response.data[1]['param_name'], 'param2')
        self.assertEqual(response.data[1]['param_description'], 'value2')


class GetStackOverflowRoutesTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        param1 = StackParams.objects.create(param_name='param1', param_description='value1')
        param2 = StackParams.objects.create(param_name='param2', param_description='value2')
        route1 = StackRoute.objects.create(route_category='category1', route_query='query1', route='route1')
        route1.params.add(param1)
        route2 = StackRoute.objects.create(route_category='category2', route_query='query2', route='route2')
        route2.params.add(param2)

    def test_get_all_routes(self):
        # Get the URL of the view
        url = reverse('GetStackOverflowRoutes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['route_category'], 'category1')
        self.assertEqual(response.data[0]['route_query'], 'query1')
        self.assertEqual(response.data[0]['route'], 'route1')
        self.assertEqual(response.data[0]['params'][0]['param_name'], 'param1')
        self.assertEqual(response.data[0]['params'][0]['param_description'], 'value1')
        self.assertEqual(response.data[1]['route_category'], 'category2')
        self.assertEqual(response.data[1]['route_query'], 'query2')
        self.assertEqual(response.data[1]['route'], 'route2')
        self.assertEqual(response.data[1]['params'][0]['param_name'], 'param2')
        self.assertEqual(response.data[1]['params'][0]['param_description'], 'value2')


class GetAllStackOverflowFiltersTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create some sample StackFilters
        StackFilters.objects.create(filter_name='filter1', filter_description='value1')
        StackFilters.objects.create(filter_name='filter2', filter_description='value2')

    def test_get_all_filters(self):
        url = reverse('GetAllStackOverflowFilters')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['filter_name'], 'filter1')
        self.assertEqual(response.data[0]['filter_description'], 'value1')
        self.assertEqual(response.data[1]['filter_name'], 'filter2')
        self.assertEqual(response.data[1]['filter_description'], 'value2')


class GetStackOverflowSortMethodsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        StackSortMethods.objects.create(sort_name='method1', sort_description='description1')
        StackSortMethods.objects.create(sort_name='method2', sort_description='description2')

    def test_get_all_sort_methods(self):
        # Get the URL of the view
        url = reverse('GetStackOverflowSortMethods')  # Replace with the actual name of the view in your URL configuration
        # Send a GET request to the view
        response = self.client.get(url)
        # Check that the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check that the number of sort methods returned is correct
        self.assertEqual(len(response.data), 2)
        # Check that the sort_name and sort_description of the sort methods are correct
        self.assertEqual(response.data[0]['sort_name'], 'method1')
        self.assertEqual(response.data[0]['sort_description'], 'description1')
        self.assertEqual(response.data[1]['sort_name'], 'method2')
        self.assertEqual(response.data[1]['sort_description'], 'description2')


class GetStackOverflowOrderMethodsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        StackOrderMethods.objects.create(order_name='order1', order_description='description1')
        StackOrderMethods.objects.create(order_name='order2', order_description='description2')

    def test_get_all_order_methods(self):
        url = reverse('GetStackOverflowOrderMethods')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['order_name'], 'order1')
        self.assertEqual(response.data[0]['order_description'], 'description1')
        self.assertEqual(response.data[1]['order_name'], 'order2')
        self.assertEqual(response.data[1]['order_description'], 'description2')


class GetStackOverflowQuestionDataFieldsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        StackQuestionDataFields.objects.create(data_field_name='field1', data_field_description='description1')
        StackQuestionDataFields.objects.create(data_field_name='field2', data_field_description='description2')

    def test_get_all_data_fields(self):
        url = reverse('GetStackOverflowQuestionDataFields')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['data_field_name'], 'field1')
        self.assertEqual(response.data[0]['data_field_description'], 'description1')
        self.assertEqual(response.data[1]['data_field_name'], 'field2')
        self.assertEqual(response.data[1]['data_field_description'], 'description2')


class InitialiseDatabaseTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('search.views.DatabaseInitialisation')
    def test_initialise_database(self, mock_db_init):
        mock_db_init.return_value.initialiseDatabase.return_value = True
        url = reverse('InitialiseDatabase')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('search.views.DatabaseInitialisation')
    def test_initialise_database_failure(self, mock_db_init):
        mock_db_init.return_value.initialiseDatabase.return_value = False
        url = reverse('InitialiseDatabase')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetRedditDataTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('search.views.searchRedditAndReturnResponse')
    @patch('search.views.insertRedditQuestionToDB')
    @patch('django_rq.get_queue')
    def test_get_reddit_data(self, mock_get_queue, mock_insert_to_db, mock_search_reddit):
        mock_search_reddit.return_value = [{'title': 'title1', 'link': 'link1'}, {'title': 'title2', 'link': 'link2'}]
        url = reverse('GetRedditData', kwargs={'subred': 'python', 'q': 'exception', 'search_type': 'link', 'limit': '100'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = RedditSearchQuerySerializer(mock_search_reddit.return_value, many=True).data
        self.assertEqual(response.data, expected_data)