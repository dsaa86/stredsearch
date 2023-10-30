from models import *


class DatabaseInitialisation():
    def __init__(self) -> None:
        self.createStackParams()
        self.createStackSortMethods()
        self.createStackOrderMethods()
        self.createStackFilters()
        self.createStackQuestionDataFields()
        self.createStackRoute()
        self.createStackRouteMeta()


    def createStackParams(self):
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


    def createStackSortMethods(self):
        self.activity_sort = StackSortMethods.objects.get_or_create(sort_name="activity", sort_description="Sort by recent activity")
        self.votes_sort = StackSortMethods.objects.get_or_create(sort_name="votes", sort_description="Sort by number of votes")
        self.creation_sort = StackSortMethods.objects.get_or_create(sort_name="creation", sort_description="Sort by creation date")
        self.hot_sort = StackSortMethods.objects.get_or_create(sort_name="hot", sort_description="Sort by recent popularity")
        self.week_sort = StackSortMethods.objects.get_or_create(sort_name="week", sort_description="Sort by week of creation")
        self.month_sort = StackSortMethods.objects.get_or_create(sort_name="month", sort_description="Sort by month of creation")


    def createStackOrderMethods(self):  
        self.asc_order = StackOrderMethods.objects.get_or_create(order_name="asc", order_description="Sort in ascending order")
        self.desc_order = StackOrderMethods.objects.get_or_create(order_name="desc", order_description="Sort in descending order")


    def createStackFilters(self):
        self.from_date_filter = StackFilters.objects.get_or_create(filter_name="fromdate", filter_description="Unix timestamp of the minimum creation date on a returned item")
        self.to_date_filter = StackFilters.objects.get_or_create(filter_name="todate", filter_description="Unix timestamp of the maximum creation date on a returned item")
        self.min_filter = StackFilters.objects.get_or_create(filter_name="min", filter_description="Minimum of the range to include in the response")
        self.max_filter = StackFilters.objects.get_or_create(filter_name="max", filter_description="Maximum of the range to include in the response")
        self.page_filter = StackFilters.objects.get_or_create(filter_name="page", filter_description="The pagination offset for the current collection. Affected by the specified pagesize")
        self.pagesize_filter = StackFilters.objects.get_or_create(filter_name="pagesize", filter_description="The number of collection results to display during pagination. Should be between 0 and 100 inclusive")


    def createStackQuestionDataFields(self):
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


    def createStackRoute(self):
        self.question_by_tag_route = StackRoute.objects.get_or_create(route_category="questions", route_query="question_by_tag", route="/2.3/questions", params=[self.tagged_param])

        self.related_questions_route = StackRoute.objects.get_or_create(route_category="questions", route_query="related_questions", route="/2.3/questions/{question_ids}/related", params=[self.question_id_field])

        self.search_route = StackRoute.objects.get_or_create(route_category="search", route_query="search", route="/2.3/search", params=[self.nottagged_param, self.tagged_param, self.intitle_param])

        self.advanced_route = StackRoute.objects.get_or_create(route_category="search", route_query="advanced-search", route="/2.3/search/advanced", params=[self.question_param, self.accepted_param, self.answers_param, self.body_param, self.closed_param, self.migrated_param, self.notice_param, self.nottagged_param, self.tagged_param, self.title_param, self.user_param, self.url_param, self.views_param, self.wiki_param])


    def createStackRouteMeta(self):
        self.stack_meta = StackRouteMeta.objects.get_or_create(route_prepend="https://api.stackexchange.com", route_append="&site=stackoverflow")
