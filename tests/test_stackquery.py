from  stredsearch.search.custom_functionality  import stackquery

class TestStackQuery:

    def test_getQueryCategories(self):

        function_response = stackquery.getQueryCategories()
        access_route_keys = stackquery.ACCESS_ROUTES.keys()
        cat_type_check = True

        for cat in function_response:
            if type(cat) is not str:
                cat_type_check = False

        assert cat_type_check is True
        assert type(function_response) is list
        assert type(function_response) is not dict
        assert 'meta' not in function_response
        assert len(access_route_keys) != len(function_response)
        assert len(function_response) == (len(access_route_keys) - 1)

    def test_getQueryCategoryRoutes(self):

        function_response = stackquery.getQueryCategoryRoutes('questions')
        access_route_keys = stackquery.ACCESS_ROUTES['questions'].keys()
        questions_function_len = len(function_response)
        questions_raw_len = len(access_route_keys)
        route_type_check = True

        for route in function_response:
            if type(route) is not str:
                route_type_check = False

        assert type(function_response) is list
        assert type(function_response) is not dict
        assert route_type_check is True
        assert questions_function_len == questions_raw_len

    def test_getAPIRoute(self):
        function_response = stackquery.getAPIRoute('questions', 'question_by_tag')

        assert type(function_response) is str
        assert function_response == stackquery.ACCESS_ROUTES['questions']['question_by_tag']['route']
        assert '2.3' in function_response

    def test_getAPIParams(self):
        function_response = stackquery.getAPIParams('questions', 'question_by_tag')

        assert type(function_response) is dict
        assert 'tagged' in function_response.keys()

    def test_getRoutePrepend(self):
        function_response = stackquery.getRoutePrepend()

        assert type(function_response) is str
        assert function_response is stackquery.ACCESS_ROUTES['meta']['route_prepend']

    def test_getRouteAppend(self):
        function_response = stackquery.getRouteAppend()

        assert type(function_response) is dict
        assert len(function_response) is 1
        assert 'site' in function_response.keys()
        assert function_response['site'] is 'stackoverflow'

    def test_getDictOfPossibleFilters(self):
        function_response = stackquery.getFilters()
        filters = ['fromdate', 'todate', 'min', 'max', 'page', 'pagesize', 'order', 'sort']
        all_filters_present = True

        for filter in filters:
            if filter not in function_response.keys():
                all_filters_present = False

        assert type(function_response) is dict
        assert len(function_response) == len(stackquery.ACCESS_ROUTES['meta']['filters'])
        assert all_filters_present == True
        assert "fromdate" in function_response.keys()


    filters = {
        'page' : '1',
        'pageSize' : None,
        'tagged' : "python;java"
    }

    def test_processUserChosenFilters(self):
        pass

    def test_sanitise_stack_overflow_response(self):
        pass