import os
import sys
from unittest.mock import Mock, patch

from django.test import TestCase
from search.models import StackQuestion
from search.tasks import (UnsuccessfulDBSave, insertRedditQuestionToDB,
                          insertStackQuestionsToDB, insertStackTagsToDB)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class InsertStackQuestionsToDBTest(TestCase):
    @patch('search.tasks.removeNaiveTzFromDatetime')
    @patch('search.tasks.createStubsForMissingData')
    @patch('search.tasks.sanitiseTagStringToList')
    @patch('search.tasks.StackQuestion.objects.filter')
    @patch('search.tasks.updateQuestionParamsInDB')
    @patch('search.tasks.retrieveUserFromDB')
    @patch('search.tasks.retrieveTagsFromDB')
    @patch('search.tasks.retrieveSearchTermFromDB')
    @patch('search.tasks.createNewStackQuestionInDB')
    def test_insertStackQuestionsToDB(self, mock_create_new, mock_retrieve_search_term, mock_retrieve_tags, mock_retrieve_user, mock_update, mock_filter, mock_sanitise, mock_create_stubs, mock_remove_naive):
        mock_question_set = [{'question_id': '1', 'tags': 'tag1,tag2', 'user_id': '1', 'display_name': 'user1'}]
        mock_filter.return_value.count.return_value = 0
        mock_sanitise.return_value = 'tag1,tag2'
        mock_retrieve_user.return_value = Mock()
        mock_retrieve_tags.return_value = [Mock(), Mock()]
        mock_retrieve_search_term.return_value = Mock()
        mock_create_new.return_value = Mock()
        mock_create_stubs.return_value = {'question_id': '1', 'tags': 'tag1,tag2', 'user_id': '1', 'display_name': 'user1', 'other_key': 'other_value'}
        insertStackQuestionsToDB(mock_question_set)
        mock_remove_naive.assert_called_once_with(mock_question_set[0])
        mock_create_stubs.assert_called_once_with(mock_remove_naive.return_value)
        mock_sanitise.assert_called_once_with(mock_create_stubs.return_value['tags'])
        mock_filter.assert_called_once_with(question_id=mock_create_stubs.return_value["question_id"])
        mock_retrieve_user.assert_called_once_with(mock_create_stubs.return_value['user_id'], mock_create_stubs.return_value['display_name'])
        mock_retrieve_tags.assert_called_once_with(mock_sanitise.return_value)
        mock_retrieve_search_term.assert_called_once_with(mock_create_stubs.return_value)
        mock_create_new.assert_called_once_with(mock_create_stubs.return_value, mock_retrieve_user.return_value, mock_retrieve_tags.return_value, [mock_retrieve_search_term.return_value])


# class InsertStackTagsToDBTest(TestCase):
#     @patch('search.tasks.StackTags.objects.get_or_create')
#     @patch('search.tasks.StackQuestion.objects.filter')
#     @patch('search.tasks.StackTags.objects.get')
#     @patch('search.tasks.StackTags.objects.filter')
#     @patch('search.tasks.StackTags.objects.all')
#     def test_insertStackTagsToDB(self, mock_all, mock_filter, mock_get, mock_filter_question, mock_get_or_create):
#         mock_data = [{'tag_name': 'tag1', 'number_of_instances_on_so': 1}, {'tag_name': 'tag2', 'number_of_instances_on_so': 2}]
#         mock_all.return_value = [Mock(tag_name='tag1'), Mock(tag_name='tag2')]
#         mock_filter.return_value.exists.return_value = True
#         mock_get.return_value = Mock(tag_name='tag1', number_of_instances_on_so=1, number_of_cached_instances=0)
#         mock_filter_question.return_value.count.return_value = 1
#         insertStackTagsToDB(mock_data)
#         mock_filter.assert_any_call(tag_name='tag1')
#         mock_get.assert_called_once_with(tag_name='tag1')
#         mock_filter_question.assert_called_once_with(tags__tag_name='tag1')
#         mock_get_or_create.assert_called_once_with(tag_name='tag2', number_of_instances_on_so=2)


class InsertRedditQuestionToDBTest(TestCase):
    @patch('search.tasks.retrieveSearchTermFromDB')
    @patch('search.tasks.createOrUpdateRedditQuestion')
    @patch('search.tasks.addSearchTypeToRedditQuestion')
    def test_insertRedditQuestionToDB(self, mock_add_search_type, mock_create_or_update, mock_retrieve_search_term):
        # Set up the mock objects
        mock_data = {
            'search_term': 'test',
            'question_set': [{'link': 'link1', 'title': 'title1'}, {'link': 'link2', 'title': 'title2'}],
            'search_type_set': 'type1,type2'
        }
        mock_retrieve_search_term.return_value = Mock()
        mock_create_or_update.return_value = True
        mock_add_search_type.return_value = True
        # Call the function
        result = insertRedditQuestionToDB(mock_data)
        # Check that the mock functions were called with the correct arguments
        mock_retrieve_search_term.assert_called_once_with({'q': mock_data['search_term']})
        mock_create_or_update.assert_any_call(mock_data['question_set'][0]['link'], mock_data['question_set'][0]['title'], mock_retrieve_search_term.return_value)
        mock_create_or_update.assert_any_call(mock_data['question_set'][1]['link'], mock_data['question_set'][1]['title'], mock_retrieve_search_term.return_value)
        mock_add_search_type.assert_any_call(mock_data['search_type_set'].split(','), mock_data['question_set'][0]['link'])
        mock_add_search_type.assert_any_call(mock_data['search_type_set'].split(','), mock_data['question_set'][1]['link'])
        # Check that the function returned True
        self.assertEqual(result, True)

    def test_insertRedditQuestionToDB_unsuccessful_save(self):
        # Set up the mock objects
        mock_data = {
            'search_term': 'test',
            'question_set': [{'link': 'link1', 'title': 'title1'}, {'link': 'link2', 'title': 'title2'}],
            'search_type_set': 'type1,type2'
        }
        with patch('search.tasks.retrieveSearchTermFromDB') as mock_retrieve_search_term, \
             patch('search.tasks.createOrUpdateRedditQuestion', return_value=False) as mock_create_or_update, \
             patch('search.tasks.addSearchTypeToRedditQuestion') as mock_add_search_type:
            # Call the function and check that it raises an UnsuccessfulDBSave exception
            with self.assertRaises(UnsuccessfulDBSave):
                insertRedditQuestionToDB(mock_data)