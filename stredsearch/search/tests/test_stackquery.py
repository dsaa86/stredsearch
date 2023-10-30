from lib2to3.pytree import convert

from stackquery import *
from django.test import TestCase


# Create your tests here.
class TestStackQuery(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.sanitiseTestData = {
            'items': [
                {
                    'tags': 
                        ['python', 'pygame'],
                    'owner': {
                        'account_id': 29127741,
                        'reputation': 9, 
                        'user_id': 22313711, 
                        'user_type': 
                        'registered', 
                        'profile_image': 'https://lh3.googleusercontent.com/a/AAcHTtcoWqgi1AuJtw2Y5gvmpDMno3ky_hb7J-sprJBNT6DUiwE=k-s256', 
                        'display_name': 'Beanss', 
                        'link': 'https://stackoverflow.com/users/22313711/beanss'
                    }, 
                    'is_answered': False, 
                    'view_count': 15, 
                    'closed_date': 1698651661, 
                    'answer_count': 0, 
                    'score': -1, 
                    'last_activity_date': 1698651714, 
                    'creation_date': 1698628269, 
                    'last_edit_date': 1698651714, 
                    'question_id': 77385782, 
                    'link': 'https://stackoverflow.com/questions/77385782/how-do-i-make-the-game-over-title-hover-up-and-down',
                    'closed_reason': 'Duplicate', 
                    'title': 'How do I make the Game Over title hover up and down?'
                }, 
                {
                    'tags': ['python', 'base64', 'animated-gif'], 'owner': {
                        
                        'account_id': 15797258, 
                        'reputation': 350, 
                        'user_id': 11398747, 
                        'user_type': 'registered', 
                        'profile_image': 'https://lh4.googleusercontent.com/-c1AEHYfVwQo/AAAAAAAAAAI/AAAAAAAAAAA/ACHi3rf0x4NnedYPXADJ7R9MCtdbXqWKyg/mo/photo.jpg?sz=256', 
                        'display_name': 'Travis Tay', 
                        'link': 'https://stackoverflow.com/users/11398747/travis-tay'
                    }, 
                    'is_answered': False, 
                    'view_count': 343, 
                    'answer_count': 1, 
                    'score': 0, 
                    'last_activity_date': 1698651706, 
                    'creation_date': 1590421576, 
                    'last_edit_date': 1698651706, 
                    'question_id': 62006013, 
                    'content_license': 'CC BY-SA 4.0', 
                    'link': 'https://stackoverflow.com/questions/62006013/gif-to-base64-encoding-without-saving-file', 
                    'title': 'Gif to base64 encoding without saving file'
                }
            ]
        }

        self.sanitiseTestExpectedResponse = [
            {
                'tags': 
                    ['python', 'pygame'],
                'owner': {
                    'account_id': 29127741,
                    'reputation': 9, 
                    'user_id': 22313711, 
                    'user_type': 
                    'registered', 
                    'profile_image': 'https://lh3.googleusercontent.com/a/AAcHTtcoWqgi1AuJtw2Y5gvmpDMno3ky_hb7J-sprJBNT6DUiwE=k-s256', 
                    'display_name': 'Beanss', 
                    'link': 'https://stackoverflow.com/users/22313711/beanss'
                }, 
                'is_answered': False, 
                'view_count': 15, 
                'closed_date': 1698651661, 
                'answer_count': 0, 
                'score': -1, 
                'last_activity_date': 1698651714, 
                'creation_date': 1698628269, 
                'last_edit_date': 1698651714, 
                'question_id': 77385782, 
                'link': 'https://stackoverflow.com/questions/77385782/how-do-i-make-the-game-over-title-hover-up-and-down',
                'closed_reason': 'Duplicate', 
                'title': 'How do I make the Game Over title hover up and down?'
            }, 
            {
                'tags': ['python', 'base64', 'animated-gif'], 'owner': {
                    
                    'account_id': 15797258, 
                    'reputation': 350, 
                    'user_id': 11398747, 
                    'user_type': 'registered', 
                    'profile_image': 'https://lh4.googleusercontent.com/-c1AEHYfVwQo/AAAAAAAAAAI/AAAAAAAAAAA/ACHi3rf0x4NnedYPXADJ7R9MCtdbXqWKyg/mo/photo.jpg?sz=256', 
                    'display_name': 'Travis Tay', 
                    'link': 'https://stackoverflow.com/users/11398747/travis-tay'
                }, 
                'is_answered': False, 
                'view_count': 343, 
                'answer_count': 1, 
                'score': 0, 
                'last_activity_date': 1698651706, 
                'creation_date': 1590421576, 
                'last_edit_date': 1698651706, 
                'question_id': 62006013, 
                'content_license': 'CC BY-SA 4.0', 
                'link': 'https://stackoverflow.com/questions/62006013/gif-to-base64-encoding-without-saving-file', 
                'title': 'Gif to base64 encoding without saving file'
            }
        ]


    def testGetRoutePrepend(self):
        self.assertEqual(getRoutePrepend(), "https://api.stackexchange.com/2.2/")
        self.assertEqual(type(getRoutePrepend()), str)

    def testGetAPIRoute(self):
        self.assertEqual(getAPIRoute("questions", "question_by_tag"), "/2.3/questions")
        self.assertEqual(getAPIRoute("search", "advanced_search"), "/2.3/search/advanced")

    def testGetRouteAppend(self):
        self.assertEqual(getRouteAppend(), "&site=stackoverflow")
        self.assertEqual(type(getRouteAppend()), str)

    def testSanitiseStackOverflowResponse(self):
        with self.assertRaises(TypeError):
            sanitiseStackOverflowResponse("test")
            sanitiseStackOverflowResponse(1)
            sanitiseStackOverflowResponse(1.0)
            sanitiseStackOverflowResponse(True)
            sanitiseStackOverflowResponse(False)
            sanitiseStackOverflowResponse(None)
            sanitiseStackOverflowResponse(["test"])

        self.assertEqual(sanitiseStackOverflowResponse({"items": [{"title": "test title", "link": "test link"}]}), [{"title": "test title", "link": "test link"}])

        self.assertEqual(type(sanitiseStackOverflowResponse(self.sanitiseTestData)), list)

    def testGetOnlyQuestionsFromStackOverflowResponse(self):
        with self.assertRaises(TypeError):
            getOnlyQuestionsFromStackOverflowResponse("test")
            getOnlyQuestionsFromStackOverflowResponse(1)
            getOnlyQuestionsFromStackOverflowResponse(1.0)
            getOnlyQuestionsFromStackOverflowResponse(True)
            getOnlyQuestionsFromStackOverflowResponse(False)
            getOnlyQuestionsFromStackOverflowResponse(None)
            getOnlyQuestionsFromStackOverflowResponse(["test"])

        with self.assertRaises(KeyError):
            getOnlyQuestionsFromStackOverflowResponse({"items": [{"title": "test title", "link": "test link"}]})
            getOnlyQuestionsFromStackOverflowResponse({"items": [{"title": "test title", "link": "test link"}, {"title": "test title 2", "link": "test link 2"}]})
        
        with self.assertRaises(ValueError):
            getOnlyQuestionsFromStackOverflowResponse({"items": []})

        self.assertEqual(getOnlyQuestionsFromStackOverflowResponse(self.sanitiseTestData), self.sanitiseTestExpectedResponse)

        self.assertNotEqual(type(getOnlyQuestionsFromStackOverflowResponse(self.sanitiseTestData)), dict)

    def testGetQuestionData(self):
        with self.assertRaises(TypeError):
            # Is param not of type dict
            getQuestionData("test")
            getQuestionData(1)
            getQuestionData(1.0)
            getQuestionData(True)
            getQuestionData(False)
            getQuestionData(None)
            getQuestionData(["test"])
            # Is param["tags"] not of type list
            getQuestionData({"title": "test title", "tags": "test tag"})
            getQuestionData({"title": "test title", "tags": 1})
            getQuestionData({"title": "test title", "tags": 1.0})
            getQuestionData({"title": "test title", "tags": True})
            getQuestionData({"title": "test title", "tags": False})
            getQuestionData({"title": "test title", "tags": None})
            getQuestionData({"title": "test title", "tags": {"test tag"}})
            # Is param["owner"] not of type dict
            getQuestionData({"title": "test title", "owner": ["test owner"]})
            getQuestionData({"title": "test title", "owner": "test owner"})
            getQuestionData({"title": "test title", "owner": 1})
            getQuestionData({"title": "test title", "owner": 1.0})
            getQuestionData({"title": "test title", "owner": True})
            getQuestionData({"title": "test title", "owner": False})
            getQuestionData({"title": "test title", "owner": None})

        with self.assertRaises(KeyError):
            # Param not containing key "tags"
            getQuestionData({"title": "test title", "link": "test link", "owner": {"display_name": "test display name"}})
            # Param not containing key "owner"
            getQuestionData({"title": "test title", "link": "test link", "tags" : ["tag1", "tag2"]})

        self.assertEqual(getQuestionData(self.sanitiseTestExpectedResponse[0]), {
            'tags': 'python,pygame', 
            'user_id': 22313711, 
            'display_name': 'Beanss',
            'is_answered': False, 
            'view_count': 15,
            'answer_count': 0, 
            'score': -1, 
            'last_activity_date': 1698651714, 
            'creation_date': 1698628269, 
            'last_edit_date': 1698651714, 
            'question_id': 77385782, 
            'link': 'https://stackoverflow.com/questions/77385782/how-do-i-make-the-game-over-title-hover-up-and-down',
            'title': 'How do I make the Game Over title hover up and down?'
        })


    def testConvertListToString(self):
        with self.assertRaises(TypeError):
            convertListToString("test")
            convertListToString(1)
            convertListToString(1.0)
            convertListToString(True)
            convertListToString(False)
            convertListToString(None)
            convertListToString(["test"])
            convertListToString(["test"], 1)
            convertListToString(["test"], 1.0)
            convertListToString(["test"], True)
            convertListToString(["test"], False)
            convertListToString(["test"], None)
            convertListToString(["test"], ["test"])
            convertListToString(["test"], {"test"})
            convertListToString(["test"], {"test": "test"})
            convertListToString(["test"], " ")
            convertListToString(["test"], "1")

        self.assertEqual(convertListToString(["test"], ","), "test")
        self.assertEqual(convertListToString(["test", "test2"], ","), "test,test2")
        self.assertEqual(convertListToString(["test", "test2", "test3"]), "testtest2test3")


    def testExtractOwnerData(self):
        with self.assertRaises(TypeError):
            # Question param is not dict
            extractOwnerData("test", "test")
            extractOwnerData(1, "test")
            extractOwnerData(1.0, "test")
            extractOwnerData(True, "test")
            extractOwnerData(False, "test")
            extractOwnerData(None, "test")
            # Key param is not string
            extractOwnerData({"test": "test"}, 1)
            extractOwnerData({"test": "test"}, 1.0)
            extractOwnerData({"test": "test"}, True)
            extractOwnerData({"test": "test"}, False)
            extractOwnerData({"test": "test"}, None)
            extractOwnerData({"test": "test"}, ["test"])
            extractOwnerData({"test": "test"}, {"test"})
            # Question["owner"] is not dict
            extractOwnerData({"test" : "test", "owner" : "owner"}, "test")
            extractOwnerData({"test" : "test", "owner" : 1}, "test")
            extractOwnerData({"test" : "test", "owner" : 1.0}, "test")
            extractOwnerData({"test" : "test", "owner" : True}, "test")
            extractOwnerData({"test" : "test", "owner" : False}, "test")
            extractOwnerData({"test" : "test", "owner" : None}, "test")
            extractOwnerData({"test" : "test", "owner" : ["test"]}, "test")
            # Question["owner"][key] is not string
            extractOwnerData({"test" : "test", "owner" : {"test": 1}}, "test")
            extractOwnerData({"test" : "test", "owner" : {"test": 1.0}}, "test")
            extractOwnerData({"test" : "test", "owner" : {"test": True}}, "test")
            extractOwnerData({"test" : "test", "owner" : {"test": False}}, "test")
            extractOwnerData({"test" : "test", "owner" : {"test": None}}, "test")
            extractOwnerData({"test" : "test", "owner" : {"test": ["test"]}}, "test")
            extractOwnerData({"test" : "test", "owner" : {"test": {"test"}}}, "test")

        with self.assertRaises(KeyError):
            # Question param does not contain key "owner"
            extractOwnerData({"test" : "test"}, "test")
            # Question["owner"] does not contain key "test"
            extractOwnerData({"test" : "test", "owner" : {"test2": "test"}}, "test")

        with self.assertRaises(ValueError):
            # Question["owner"][key] is empty string
            extractOwnerData({"test" : "test", "owner" : {"test": ""}}, "test")

        self.assertEqual(extractOwnerData({"test" : "test", "owner" : {"user_id": "sample user id"}}, "user_id"), "sample user id")

        self.assertEqual(extractOwnerData({"test" : "test", "owner" : {"display_name": "sample display name"}}, "display_name"), "sample display name")


    def testExtractRelevantQuestionDataFieldsForQuestion(self):
        with self.assertRaises(TypeError):
            # Param is not dict
            extractRelevantQuestionDataFieldsForQuestion("test")
            extractRelevantQuestionDataFieldsForQuestion(1)
            extractRelevantQuestionDataFieldsForQuestion(1.0)
            extractRelevantQuestionDataFieldsForQuestion(True)
            extractRelevantQuestionDataFieldsForQuestion(False)
            extractRelevantQuestionDataFieldsForQuestion(None)
            extractRelevantQuestionDataFieldsForQuestion(["test"])

        self.assertEqual(extractRelevantQuestionDataFieldsForQuestion({"test": "test"}), {})

        self.assertEqual(extractRelevantQuestionDataFieldsForQuestion({"is_answered" : True, "answer_count" : 2, "question_id" : 123456789}), {"is_answered" : "is_answered", "answer_count" : "answer_count", "question_id" : "question_id"})

        self.assertEqual(extractRelevantQuestionDataFieldsForQuestion({"is_answered" : True, "answer_count" : 2, "question_id" : 123456789, "date_closed" : 1234578654}), {"is_answered" : "is_answered", "answer_count" : "answer_count", "question_id" : "question_id"})

    def testGetQuestionDataFields(self):
        self.assertEqual(getQuestionDataFields(), ["is_answered", "view_count", "answer_count", "score", "last_activity_date", "creation_date", "last_edit_date", "question_id", "link", "title"])

        self.assertEqual(type(getQuestionDataFields()), list)


    def testConvertMSToDateTime(self):
        with self.assertRaises(TypeError):
            # Param is not int
            convertMSToDateTime("test")
            convertMSToDateTime(1.0)
            convertMSToDateTime(True)
            convertMSToDateTime(False)
            convertMSToDateTime(None)
            convertMSToDateTime(["test"])
            convertMSToDateTime({"test"})

        self.assertEqual(convertMSToDateTime(1634217600), datetime.datetime(2021, 10, 14, 0, 0))