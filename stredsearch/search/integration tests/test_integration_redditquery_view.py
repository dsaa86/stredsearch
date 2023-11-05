import os
import sys
from unittest.mock import MagicMock, patch

from django.test import Client, TestCase
from search.redditquery import buildTermsFromParams
from search.tasks import insertRedditQuestionToDB

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestRedditQueryIntegration(TestCase):

    def setUp(self):
        self.client = Client()

    @patch('django_rq.get_queue', return_value=MagicMock())
    def test_integration_with_buildTermsFromParams(self, mock_get_queue):
        response = self.client.get('/reddit/get/query/link/subredditname/python/10/')
        self.assertEqual(response.status_code, 200)

        expected_args = {
            "search_term" : "python",
            "search_type_set" : "link",
            "question_set" : [
                {
                    "title" : "SPAM",
                    "link" : "https://www.reddit.com/r/SUBREDDITNAME/comments/454npv/spam/",
                }
            ]
        }

        mock_queue = mock_get_queue.return_value
        mock_queue.enqueue.assert_called_once_with(insertRedditQuestionToDB, expected_args)