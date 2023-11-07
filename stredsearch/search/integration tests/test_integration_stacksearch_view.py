from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from search.models import StackQuestion

class TestGetStackOverflowQuestionsByTag(TestCase):

    def setUp(self):
        self.client = Client()

    @patch('django_rq.get_queue', return_value=MagicMock())
    @patch('search.views.queryStackOverflow')
    def test_get(self, mock_queryStackOverflow, mock_get_queue):
        # Setup
        mock_queryStackOverflow.return_value = []
        mock_get_queue.return_value.enqueue.return_value = None

        # Execute
        response = self.client.get('/stackoverflow/questions/tag/1/10/1622527200/1625119200/asc/activity/python/')

        # Assert
        self.assertEqual(response.status_code, 200)
        mock_queryStackOverflow.assert_called_once_with("questions", "question_by_tag", {
            "page": "1",
            "pagesize": "10",
            "fromdate": "1622527200",
            "todate": "1625119200",
            "order": "asc",
            "sort": "activity",
            "tagged": "python",
        })
        mock_get_queue.assert_called_once_with("default", autocommit=True, is_async=True)
        mock_get_queue.return_value.enqueue.assert_called_once()