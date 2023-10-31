from xmlrpc.client import Boolean

from search.models import *


class DatabaseInitialisation():
    def __init__(self) -> None:
        pass

    def initialiseDatabase(self) -> Boolean:

        success = True

        if not self.createStackParams():
            success = False
        if not self.createStackSortMethods():
            success = False
        if not self.createStackOrderMethods():
            success = False
        if not self.createStackFilters():
            success = False
        if not self.createStackQuestionDataFields():
            success = False
        if not self.createStackRoute():
            success = False
        if not self.createStackRouteMeta():
            success = False
            
        return success


    def createStackParams(self):
        try:
            self.question_param = StackParams.objects.get_or_create(param_name="q", param_description="Free-form text. A question asked on Stack Overflow")
            self.accepted_param = StackParams.objects.get_or_create(param_name="accepted", param_description="True to return only questions with accepted answers, false to return only those without. Omit to elide constraint")
            self.answers_param = StackParams.objects.get_or_create(param_name="answers", param_description="The minimum number of answers returned questions must have")
            self.body_param = StackParams.objects.get_or_create(param_name="body", param_description="Text which must appear in returned questions' bodies")
            self.closed_param = StackParams.objects.get_or_create(param_name="closed", param_description="True to return only closed questions, false to return only open ones. Omit to elide constraint")
            self.migrated_param = StackParams.objects.get_or_create(param_name="migrated", param_description="True to return only questions migrated away from a site, false to return only those not. Omit to elide constraint")
            self.notice_param = StackParams.objects.get_or_create(param_name="notice", param_description="True to return only questions with post notices, false to return only those without. Omit to elide constraint")
            self.nottagged_param = StackParams.objects.get_or_create(param_name="nottagged", param_description="List of tags questions must not have")
            self.tagged_param = StackParams.objects.get_or_create(param_name="tagged", param_description="List of tags questions must have")
            self.title_param = StackParams.objects.get_or_create(param_name="title", param_description="Text which must appear in returned questions' titles")
            self.user_param = StackParams.objects.get_or_create(param_name="user", param_description="The id of the user who must own the questions returned")
            self.url_param = StackParams.objects.get_or_create(param_name="url", param_description="A url which must be contained in a post, may include a wildcard")
            self.views_param = StackParams.objects.get_or_create(param_name="views", param_description="The minimum number of views returned questions must have")
            self.wiki_param = StackParams.objects.get_or_create(param_name="wiki", param_description="True to return only community wiki questions, false to return only non-community wiki ones. Omit to elide constraint")
            self.intitle_param = StackParams.objects.get_or_create(param_name="intitle", param_description="A string that must appear verbatim in the title of a question")
            self.blank_param = StackParams.objects.get_or_create(param_name="Blank", param_description="Blank")

            return True
        except Exception as e:
            print(e)
            return False

    def createStackSortMethods(self):
        try:
            self.activity_sort = StackSortMethods.objects.get_or_create(sort_name="activity", sort_description="Sort by recent activity")
            self.votes_sort = StackSortMethods.objects.get_or_create(sort_name="votes", sort_description="Sort by number of votes")
            self.creation_sort = StackSortMethods.objects.get_or_create(sort_name="creation", sort_description="Sort by creation date")
            self.hot_sort = StackSortMethods.objects.get_or_create(sort_name="hot", sort_description="Sort by recent popularity")
            self.week_sort = StackSortMethods.objects.get_or_create(sort_name="week", sort_description="Sort by week of creation")
            self.month_sort = StackSortMethods.objects.get_or_create(sort_name="month", sort_description="Sort by month of creation")
            return True
        except Exception as e:
            print(e)
            return False


    def createStackOrderMethods(self): 
        try:
            self.asc_order = StackOrderMethods.objects.get_or_create(order_name="asc", order_description="Sort in ascending order")
            self.desc_order = StackOrderMethods.objects.get_or_create(order_name="desc", order_description="Sort in descending order")
            return True
        except Exception as e:
            print(e)
            return False


    def createStackFilters(self):
        try:
            self.from_date_filter = StackFilters.objects.get_or_create(filter_name="fromdate", filter_description="Unix timestamp of the minimum creation date on a returned item")
            self.to_date_filter = StackFilters.objects.get_or_create(filter_name="todate", filter_description="Unix timestamp of the maximum creation date on a returned item")
            self.min_filter = StackFilters.objects.get_or_create(filter_name="min", filter_description="Minimum of the range to include in the response")
            self.max_filter = StackFilters.objects.get_or_create(filter_name="max", filter_description="Maximum of the range to include in the response")
            self.page_filter = StackFilters.objects.get_or_create(filter_name="page", filter_description="The pagination offset for the current collection. Affected by the specified pagesize")
            self.pagesize_filter = StackFilters.objects.get_or_create(filter_name="pagesize", filter_description="The number of collection results to display during pagination. Should be between 0 and 100 inclusive")
            return True
        except Exception as e:
            print(e)
            return False


    def createStackQuestionDataFields(self):
        try:
            self.is_answered_field = StackQuestionDataFields.objects.get_or_create(data_field_name="is_answered", data_field_description="True if the question is considered answered, false otherwise")
            self.view_count_field = StackQuestionDataFields.objects.get_or_create(data_field_name="view_count", data_field_description="Number of times the question was viewed")
            self.answer_count_field = StackQuestionDataFields.objects.get_or_create(data_field_name="answer_count", data_field_description="Number of answers on the question (deleted answers are not counted)")
            self.score_field = StackQuestionDataFields.objects.get_or_create(data_field_name="score", data_field_description="Number of upvotes minus the number of downvotes on the question (deleted questions are not counted)")
            self.last_activity_date_field = StackQuestionDataFields.objects.get_or_create(data_field_name="last_activity_date", data_field_description="Date the last activity occurred on the question")
            self.creation_date_field = StackQuestionDataFields.objects.get_or_create(data_field_name="creation_date", data_field_description="Date the question was created")
            self.last_edit_date_field = StackQuestionDataFields.objects.get_or_create(data_field_name="last_edit_date", data_field_description="Date the question was last edited")
            self.question_id_field = StackQuestionDataFields.objects.get_or_create(data_field_name="question_id", data_field_description="The question's ID")
            self.link_field = StackQuestionDataFields.objects.get_or_create(data_field_name="link", data_field_description="A link to the question")
            self.title_field = StackQuestionDataFields.objects.get_or_create(data_field_name="title", data_field_description="The title of the question")
            return True
        except Exception as e:
            print(e)
            return False


    def createStackRoute(self):
        try:
            self.question_by_tag_route = StackRoute.objects.get_or_create(route_category="questions", route_query="question_by_tag", route="/2.3/questions")
            self.question_by_tag_route = StackRoute.objects.filter(route = "/2.3/questions").first()
            self.question_by_tag_route.params.add(StackParams.objects.filter(param_name="tagged").first())

            self.related_questions_route = StackRoute.objects.get_or_create(route_category="questions", route_query="related_questions", route="/2.3/questions/{question_ids}/related")
            self.related_questions_route = StackRoute.objects.filter(route="/2.3/questions/{question_ids}/related").first()
            self.related_questions_route.params.add(StackParams.objects.filter(param_name="Blank").first())

            self.search_route = StackRoute.objects.get_or_create(route_category="search", route_query="search", route="/2.3/search")
            self.search_route = StackRoute.objects.filter(route="/2.3/search").first()
            self.search_route.params.add(StackParams.objects.filter(param_name="nottagged").first())
            self.search_route.params.add(StackParams.objects.filter(param_name="tagged").first())
            self.search_route.params.add(StackParams.objects.filter(param_name="intitle").first())
            

            self.advanced_route = StackRoute.objects.get_or_create(route_category="search", route_query="advanced-search", route="/2.3/search/advanced")
            self.advanced_route = StackRoute.objects.filter(route="/2.3/search/advanced").first()
            self.advanced_route.params.add(StackParams.objects.filter(param_name="q").first())
            self.advanced_route.params.add(StackParams.objects.filter(param_name="accepted").first())
            self.advanced_route.params.add(StackParams.objects.filter(param_name="answers").first())
            self.advanced_route.params.add(StackParams.objects.filter(param_name="body").first())
            self.advanced_route.params.add(StackParams.objects.filter(param_name="closed").first())
            self.advanced_route.params.add(StackParams.objects.filter(param_name="migrated").first())
            self.advanced_route.params.add(StackParams.objects.filter(param_name="notice").first())
            self.advanced_route.params.add(StackParams.objects.filter(param_name="nottagged").first())
            self.advanced_route.params.add(StackParams.objects.filter(param_name="tagged").first())
            self.advanced_route.params.add(StackParams.objects.filter(param_name="title").first())
            self.advanced_route.params.add(StackParams.objects.filter(param_name="user").first())
            self.advanced_route.params.add(StackParams.objects.filter(param_name="url").first())
            self.advanced_route.params.add(StackParams.objects.filter(param_name="views").first())
            self.advanced_route.params.add(StackParams.objects.filter(param_name="wiki").first())

            return True
        except Exception as e:
            print(e)
            return False


    def createStackRouteMeta(self):
        try:
            self.stack_meta = StackRouteMeta.objects.get_or_create(route_prepend="https://api.stackexchange.com", route_append="stackoverflow")
            return True
        except Exception as e:
            print(e)
            return False
