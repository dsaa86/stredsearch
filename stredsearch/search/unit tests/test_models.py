import os
import sys
from datetime import datetime

from django.test import TestCase
from search.models import *

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class StackParamsTest(TestCase):
    def setUp(self):
        # Set up a test instance of StackParams
        StackParams.objects.create(param_name="Test Param", param_description="Test Description")

    def test_param_name(self):
        # Test the param_name property
        instance = StackParams.objects.get(param_name="Test Param")
        self.assertEqual(instance.param_name, "Test Param")

    def test_param_description(self):
        # Test the param_description property
        instance = StackParams.objects.get(param_name="Test Param")
        self.assertEqual(instance.param_description, "Test Description")

    def test_str_method(self):
        # Test the __str__ method
        instance = StackParams.objects.get(param_name="Test Param")
        self.assertEqual(str(instance), "Test Param")


class StackSortMethodsTest(TestCase):
    def setUp(self):
        # Set up a test instance of StackSortMethods
        StackSortMethods.objects.create(sort_name="Test Sort", sort_description="Test Description")

    def test_sort_name(self):
        # Test the sort_name property
        instance = StackSortMethods.objects.get(sort_name="Test Sort")
        self.assertEqual(instance.sort_name, "Test Sort")

    def test_sort_description(self):
        # Test the sort_description property
        instance = StackSortMethods.objects.get(sort_name="Test Sort")
        self.assertEqual(instance.sort_description, "Test Description")

    def test_str_method(self):
        # Test the __str__ method
        instance = StackSortMethods.objects.get(sort_name="Test Sort")
        self.assertEqual(str(instance), "Test Sort")


class StackOrderMethodsTest(TestCase):
    def setUp(self):
        # Set up a test instance of StackOrderMethods
        StackOrderMethods.objects.create(order_name="Test Order", order_description="Test Description")

    def test_order_name(self):
        # Test the order_name property
        instance = StackOrderMethods.objects.get(order_name="Test Order")
        self.assertEqual(instance.order_name, "Test Order")

    def test_order_description(self):
        # Test the order_description property
        instance = StackOrderMethods.objects.get(order_name="Test Order")
        self.assertEqual(instance.order_description, "Test Description")

    def test_str_method(self):
        # Test the __str__ method
        instance = StackOrderMethods.objects.get(order_name="Test Order")
        self.assertEqual(str(instance), "Test Order")


class StackFiltersTest(TestCase):
    def setUp(self):
        # Set up a test instance of StackFilters
        StackFilters.objects.create(filter_name="Test Filter", filter_description="Test Description")

    def test_filter_name(self):
        # Test the filter_name property
        instance = StackFilters.objects.get(filter_name="Test Filter")
        self.assertEqual(instance.filter_name, "Test Filter")

    def test_filter_description(self):
        # Test the filter_description property
        instance = StackFilters.objects.get(filter_name="Test Filter")
        self.assertEqual(instance.filter_description, "Test Description")

    def test_str_method(self):
        # Test the __str__ method
        instance = StackFilters.objects.get(filter_name="Test Filter")
        self.assertEqual(str(instance), "Test Filter")


class StackQuestionDataFieldsTest(TestCase):
    def setUp(self):
        # Set up a test instance of StackQuestionDataFields
        StackQuestionDataFields.objects.create(data_field_name="Test Field", data_field_description="Test Description")

    def test_data_field_name(self):
        # Test the data_field_name property
        instance = StackQuestionDataFields.objects.get(data_field_name="Test Field")
        self.assertEqual(instance.data_field_name, "Test Field")

    def test_data_field_description(self):
        # Test the data_field_description property
        instance = StackQuestionDataFields.objects.get(data_field_name="Test Field")
        self.assertEqual(instance.data_field_description, "Test Description")

    def test_str_method(self):
        # Test the __str__ method
        instance = StackQuestionDataFields.objects.get(data_field_name="Test Field")
        self.assertEqual(str(instance), "Test Field")


class StackRouteTest(TestCase):
    def setUp(self):
        # Set up a test instance of StackRoute
        param = StackParams.objects.create(param_name="Test Param", param_description="Test Description")
        self.route = StackRoute.objects.create(route_category="Test Category", route_query="Test Query", route="Test Route")
        self.route.params.add(param)

    def test_route_category(self):
        # Test the route_category property
        self.assertEqual(self.route.route_category, "Test Category")

    def test_route_query(self):
        # Test the route_query property
        self.assertEqual(self.route.route_query, "Test Query")

    def test_route(self):
        # Test the route property
        self.assertEqual(self.route.route, "Test Route")

    def test_params(self):
        # Test the params property
        param = self.route.params.all()[0]
        self.assertEqual(param.param_name, "Test Param")
        self.assertEqual(param.param_description, "Test Description")

    def test_str_method(self):
        # Test the __str__ method
        self.assertEqual(str(self.route), "Test Route")


class StackRouteTest(TestCase):
    def setUp(self):
        # Set up a test instance of StackRoute
        param = StackParams.objects.create(param_name="Test Param", param_description="Test Description")
        self.route = StackRoute.objects.create(route_category="Test Category", route_query="Test Query", route="Test Route")
        self.route.params.add(param)

    def test_route_category(self):
        # Test the route_category property
        self.assertEqual(self.route.route_category, "Test Category")

    def test_route_query(self):
        # Test the route_query property
        self.assertEqual(self.route.route_query, "Test Query")

    def test_route(self):
        # Test the route property
        self.assertEqual(self.route.route, "Test Route")

    def test_params(self):
        # Test the params property
        param = self.route.params.all()[0]
        self.assertEqual(param.param_name, "Test Param")
        self.assertEqual(param.param_description, "Test Description")

    def test_str_method(self):
        # Test the __str__ method
        self.assertEqual(str(self.route), "Test Route")


class StackRouteTest(TestCase):
    def setUp(self):
        # Set up a test instance of StackRoute
        param = StackParams.objects.create(param_name="Test Param", param_description="Test Description")
        self.route = StackRoute.objects.create(route_category="Test Category", route_query="Test Query", route="Test Route")
        self.route.params.add(param)

    def test_route_category(self):
        # Test the route_category property
        self.assertEqual(self.route.route_category, "Test Category")

    def test_route_query(self):
        # Test the route_query property
        self.assertEqual(self.route.route_query, "Test Query")

    def test_route(self):
        # Test the route property
        self.assertEqual(self.route.route, "Test Route")

    def test_params(self):
        # Test the params property
        param = self.route.params.all()[0]
        self.assertEqual(param.param_name, "Test Param")
        self.assertEqual(param.param_description, "Test Description")

    def test_str_method(self):
        # Test the __str__ method
        self.assertEqual(str(self.route), "Test Route")


class StackUserTest(TestCase):
    def setUp(self):
        # Set up a test instance of StackUser
        StackUser.objects.create(user_id=1, display_name="Test User")

    def test_user_id(self):
        # Test the user_id property
        user = StackUser.objects.get(user_id=1)
        self.assertEqual(user.user_id, 1)

    def test_display_name(self):
        # Test the display_name property
        user = StackUser.objects.get(user_id=1)
        self.assertEqual(user.display_name, "Test User")

    def test_str_method(self):
        # Test the __str__ method
        user = StackUser.objects.get(user_id=1)
        self.assertEqual(str(user), "Test User")


class StackTagsTest(TestCase):
    def setUp(self):
        # Set up a test instance of StackTags
        StackTags.objects.create(tag_name="Test Tag", number_of_instances_on_so=10, number_of_cached_instances=5)

    def test_tag_name(self):
        # Test the tag_name property
        tag = StackTags.objects.get(tag_name="Test Tag")
        self.assertEqual(tag.tag_name, "Test Tag")

    def test_number_of_instances_on_so(self):
        # Test the number_of_instances_on_so property
        tag = StackTags.objects.get(tag_name="Test Tag")
        self.assertEqual(tag.number_of_instances_on_so, 10)

    def test_number_of_cached_instances(self):
        # Test the number_of_cached_instances property
        tag = StackTags.objects.get(tag_name="Test Tag")
        self.assertEqual(tag.number_of_cached_instances, 5)

    def test_str_method(self):
        # Test the __str__ method
        tag = StackTags.objects.get(tag_name="Test Tag")
        self.assertEqual(str(tag), "Test Tag")


class SearchTermsTest(TestCase):
    def setUp(self):
        # Set up a test instance of SearchTerms
        SearchTerms.objects.create(search_term="Test Search Term")

    def test_search_term(self):
        # Test the search_term property
        search_term = SearchTerms.objects.get(search_term="Test Search Term")
        self.assertEqual(search_term.search_term, "Test Search Term")

    def test_str_method(self):
        # Test the __str__ method
        search_term = SearchTerms.objects.get(search_term="Test Search Term")
        self.assertEqual(str(search_term), "Test Search Term")


class StredSearchQuestionTest(TestCase):
    def setUp(self):
        # Set up a test instance of StredSearchQuestion
        search_term = SearchTerms.objects.create(search_term="Test Search Term")
        self.question = StredSearchQuestion.objects.create(link="Test Link", title="Test Title")
        self.question.search_term.add(search_term)

    def test_link(self):
        # Test the link property
        self.assertEqual(self.question.link, "Test Link")

    def test_title(self):
        # Test the title property
        self.assertEqual(self.question.title, "Test Title")

    def test_times_returned_as_search_result(self):
        # Test the times_returned_as_search_result property
        self.assertEqual(self.question.times_returned_as_search_result, 0)

    def test_search_term(self):
        # Test the search_term property
        search_term = self.question.search_term.all()[0]
        self.assertEqual(search_term.search_term, "Test Search Term")

    def test_created_on_stredsearch(self):
        # Test the created_on_stredsearch property
        self.assertIsInstance(self.question.created_on_stredsearch, datetime)

    def test_updated_on_stredsearch(self):
        # Test the updated_on_stredsearch property
        self.assertIsInstance(self.question.updated_on_stredsearch, datetime)

    def test_str_method(self):
        # Test the __str__ method
        self.assertEqual(str(self.question), self.question.title)


class StackQuestionTest(TestCase):
    def setUp(self):
        # Set up a test instance of StackQuestion
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

    def test_owner(self):
        # Test the owner property
        self.assertEqual(self.question.owner.user_id, 1)

    def test_is_answered(self):
        # Test the is_answered property
        self.assertEqual(self.question.is_answered, False)

    def test_view_count(self):
        # Test the view_count property
        self.assertEqual(self.question.view_count, 100)

    def test_answer_count(self):
        # Test the answer_count property
        self.assertEqual(self.question.answer_count, 5)

    def test_score(self):
        # Test the score property
        self.assertEqual(self.question.score, 10)

    def test_last_activity_date(self):
        # Test the last_activity_date property
        self.assertIsInstance(self.question.last_activity_date, datetime)

    def test_creation_date(self):
        # Test the creation_date property
        self.assertIsInstance(self.question.creation_date, datetime)

    def test_question_id(self):
        # Test the question_id property
        self.assertEqual(self.question.question_id, 1)

    def test_tags(self):
        # Test the tags property
        tag = self.question.tags.all()[0]
        self.assertEqual(tag.tag_name, "Test Tag")

    def test_str_method(self):
        # Test the __str__ method
        self.assertEqual(str(self.question), str(self.question.question_id))


class RedditSearchTypeTest(TestCase):
    def setUp(self):
        # Set up a test instance of RedditSearchType
        RedditSearchType.objects.create(search_type="Test Type")

    def test_search_type(self):
        # Test the search_type property
        search_type = RedditSearchType.objects.get(search_type="Test Type")
        self.assertEqual(search_type.search_type, "Test Type")

    def test_str_method(self):
        # Test the __str__ method
        search_type = RedditSearchType.objects.get(search_type="Test Type")
        self.assertEqual(str(search_type), search_type.search_type)


class RedditQuestionTest(TestCase):
    def setUp(self):
        # Set up a test instance of RedditQuestion
        search_type = RedditSearchType.objects.create(search_type="Test Type")
        self.question = RedditQuestion.objects.create(link="Test Link", title="Test Title")
        self.question.search_type.add(search_type)

    def test_link(self):
        # Test the link property
        self.assertEqual(self.question.link, "Test Link")

    def test_title(self):
        # Test the title property
        self.assertEqual(self.question.title, "Test Title")

    def test_search_type(self):
        # Test the search_type property
        search_type = self.question.search_type.all()[0]
        self.assertEqual(search_type.search_type, "Test Type")

    def test_str_method(self):
        # Test the __str__ method
        self.assertEqual(str(self.question.title), self.question.title)