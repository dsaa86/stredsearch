import stackquery

class TestStackQuery:

    def test_getQueryCategories(self):

        function_response = stackquery.getQueryCategories()
        access_route_keys = stackquery.ACCESS_ROUTES.keys()

        assert type(function_response) is list
        
        assert type(function_response) is not dict

        cat_type_check = True
        for cat in function_response:
            if type(cat) is not str:
                cat_type_check = False

        assert cat_type_check is True

        assert 'meta' not in function_response

        assert len(access_route_keys) != len(function_response)

        assert len(function_response) == (len(access_route_keys) - 1)

    def test_getQueryCategoryRoutes(self):

        function_response = stackquery.getQueryCategoryRoutes('questions')
        access_route_keys = stackquery.ACCESS_ROUTES['questions'].keys()

        assert type(function_response) is list

        assert type(function_response) is not dict

        route_type_check = True
        for route in function_response:
            if type(route) is not str:
                route_type_check = False

        assert route_type_check is True

        questions_function_len = len(function_response)

        questions_raw_len = len(access_route_keys)

        assert questions_function_len == questions_raw_len

    def test_getAPIRoute(self):
        function_response = stackquery.getAPIRoute('questions', 'question_by_tag')

        assert type(function_response) is str

        assert function_response == stackquery.ACCESS_ROUTES['questions']['question_by_tag']['route']

        assert '2.3' in function_response