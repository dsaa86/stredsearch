import os
import sys
from unittest.mock import MagicMock, patch

from django.test import TestCase
from search.redditquery import *

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestRedditQuery(TestCase):

    def setUp(self) -> None:
        super().setUp()
        

    def test_buildTermsFromParams(self):
    # Test with sample inputs
        terms = buildTermsFromParams('python', 'link', '10')
        self.assertEqual(terms, {"q": "python", "type": "link", "limit": "10"})

        # Test with different inputs
        terms = buildTermsFromParams('java', 'comment', '20')
        self.assertEqual(terms, {"q": "java", "type": "comment", "limit": "20"})

        # Test with empty string inputs
        terms = buildTermsFromParams('', '', '')
        self.assertEqual(terms, {"q": "", "type": "", "limit": ""})

        # Test with numeric inputs
        with self.assertRaises(TypeError):
            buildTermsFromParams(123, 456, 789)

        # Test with None inputs
        with self.assertRaises(TypeError):
            buildTermsFromParams(None, None, None)


    def test_buildSubredFromParams(self):
        # Test with sample input
        subreds = buildSubredFromParams('python, java, go')
        self.assertEqual(subreds, ['python', 'java', 'go'])

        # Test with single subreddit
        subreds = buildSubredFromParams('python')
        self.assertEqual(subreds, ['python'])

        # Test with empty string input

            # Test with empty string input
        subreds = buildSubredFromParams('')
        self.assertEqual(subreds, [''])

    # Test with space string input
        subreds = buildSubredFromParams(' ')
        self.assertEqual(subreds, [''])

        # Test with numeric input
        with self.assertRaises(TypeError):
            buildSubredFromParams(123)

        # Test with None input
        with self.assertRaises(TypeError):
            buildSubredFromParams(None)


    def test_buildUrl(self):
        # Test with sample inputs
        url = buildUrl({"q": "python", "type": "link", "limit": "10"}, "/r/python")
        self.assertEqual(url, "https://www.reddit.com/r/python/search?q=python&type=link&limit=10")

        # Test with different inputs
        url = buildUrl({"q": "java", "type": "comment", "limit": "20"}, "/r/java")
        self.assertEqual(url, "https://www.reddit.com/r/java/search?q=java&type=comment&limit=20")

        # Test with numeric inputs
        with self.assertRaises(TypeError):
            buildUrl(123, "/r/123")
            buildUrl(["q", "type", "limit"], "/r/123")

        # Test with None inputs
        with self.assertRaises(TypeError):
            buildUrl(None, "/r/")

        # Test with empty string inputs
        with self.assertRaises(ValueError):
            buildUrl({"q": "", "type": "comment", "limit": "100"}, "/r/")
            buildUrl({"q": "python", "type": "", "limit": "100"}, "/r/")
            buildUrl({"q": "python", "type": "comment", "limit": ""}, "/r/")

        # Test with None inputs
        with self.assertRaises(ValueError):
            buildUrl({"q": None, "type": "comment", "limit": "100"}, "/r/")
            buildUrl({"q": "python", "type": None, "limit": "100"}, "/r/")
            buildUrl({"q": "python", "type": "comment", "limit": None}, "/r/")


    def test_processTermsForUrl(self):
        # Test with sample inputs
        terms = processTermsForUrl({"q": "python", "type": "link", "limit": "10"})
        self.assertEqual(terms, "/search?q=python&type=link&limit=10")

        # Test with different inputs
        terms = processTermsForUrl({"q": "java", "type": "comment", "limit": "20"})
        self.assertEqual(terms, "/search?q=java&type=comment&limit=20")

        # Test with empty string inputs
        terms = processTermsForUrl({"q": "", "type": "", "limit": ""})
        self.assertEqual(terms, "/search?q=&type=&limit=")

        # Test with numeric inputs
        with self.assertRaises(TypeError):
            processTermsForUrl(123)

        # Test with None inputs
        with self.assertRaises(TypeError):
            processTermsForUrl(None)


    def test_parseLinksFromHtml(self):
        # Test with sample HTML
        html = """
        <html>
            <body>
                <a aria-label="Threading vs Multiprocessing in Python" class="absolute inset-0" data-testid="post-title" href="/r/programming/comments/98koue/threading_vs_multiprocessing_in_python/">
                    <span aria-hidden="" class="invisible">
                        Threading vs Multiprocessing in Python
                    </span>
                </a>
                <a aria-label="Threading in Python Code" class="absolute inset-0" data-testid="post-title" href="/r/programming/comments/16bddy5/threading_in_python_code/">
                    <span aria-hidden="" class="invisible">
                        Threading in Python Code
                    </span>
                </a>
            </body>
        </html>
        """
        links = parseLinksFromHtml(html)
        self.assertEqual(links[0]['title'], 'Threading vs Multiprocessing in Python')
        self.assertEqual(links[0]['link'], 'https://www.reddit.com/r/programming/comments/98koue/threading_vs_multiprocessing_in_python/')
        self.assertEqual(links[1]['title'], 'Threading in Python Code')
        self.assertEqual(links[1]['link'], 'https://www.reddit.com/r/programming/comments/16bddy5/threading_in_python_code/')

        # Test with empty HTML
        html = "<html><body></body></html>"
        links = parseLinksFromHtml(html)
        self.assertEqual(links, [])

        # Test with None input
        with self.assertRaises(TypeError):
            parseLinksFromHtml(None)

        # Test with none-string input
        with self.assertRaises(TypeError):
            parseLinksFromHtml(123)
            parseLinksFromHtml(123.456)
            parseLinksFromHtml([1, 2, 3])
            parseLinksFromHtml({"key": "value"})
            parseLinksFromHtml(True)


    def test_generateRedditLinkDicts(self):
        # Test with sample inputs
        extracted_tags = [{"aria-label": "Post 1", "href": "/r/python/comments/1"}, {"aria-label": "Post 2", "href": "/r/python/comments/2"}]
        links = generateRedditLinkDicts(extracted_tags)
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0]['title'], 'Post 1')
        self.assertEqual(links[0]['link'], 'https://www.reddit.com/r/python/comments/1')
        self.assertEqual(links[1]['title'], 'Post 2')
        self.assertEqual(links[1]['link'], 'https://www.reddit.com/r/python/comments/2')

        # Test with empty list
        links = generateRedditLinkDicts([])
        self.assertEqual(links, [])

        # Test with None input
        with self.assertRaises(TypeError):
            generateRedditLinkDicts(None)

        # Test with numeric input
        with self.assertRaises(TypeError):
            generateRedditLinkDicts(123)


    @patch('search.redditquery.webdriver.Chrome')
    @patch('search.redditquery.time.sleep', return_value=None)  # Mock out the sleep call
    def test_getRedditHTMLViaSelenium(self, mock_sleep, mock_chrome):
        # Mock the Chrome driver's get and page_source methods
        mock_driver = mock_chrome.return_value
        mock_driver.get.return_value = None
        mock_driver.page_source = '<html></html>'

        # Test with sample URL
        html = getRedditHTMLViaSelenium('https://www.reddit.com/r/python')
        self.assertEqual(html, '<html></html>')

        # Test with empty string URL
        with self.assertRaises(ValueError):
            getRedditHTMLViaSelenium('')
            getRedditHTMLViaSelenium(' ')

        # Test with None URL
        with self.assertRaises(TypeError):
            getRedditHTMLViaSelenium(None)

        # Test with numeric URL
        with self.assertRaises(TypeError):
            getRedditHTMLViaSelenium(123)


    @patch('search.redditquery.getRedditHTMLViaSelenium')
    @patch('search.redditquery.parseLinksFromHtml')
    @patch('search.redditquery.buildUrl')
    @patch('search.redditquery.buildSubredFromParams')
    @patch('search.redditquery.buildTermsFromParams')
    def test_searchRedditAndReturnResponse(self, mock_buildTerms, mock_buildSubred, mock_buildUrl, mock_parseLinks, mock_getHtml):
        # Mock the functions
        mock_buildTerms.return_value = "/search?q=python&type=link&limit=10"
        mock_buildSubred.return_value = ["python"]
        mock_buildUrl.return_value = "https://www.reddit.com/r/python/search?q=python&type=link&limit=10"
        mock_getHtml.return_value = "<html></html>"
        mock_parseLinks.return_value = [{"title": "Post 1", "link": "https://www.reddit.com/r/python/comments/1"}]

        # Test with sample inputs
        results = searchRedditAndReturnResponse("python", "link", "10", "python")
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Post 1')
        self.assertEqual(results[0]['link'], 'https://www.reddit.com/r/python/comments/1')

        # Test with empty string inputs
        with self.assertRaises(ValueError):
            searchRedditAndReturnResponse("", "test", "test", "test")
            searchRedditAndReturnResponse("test", "", "test", "test")
            searchRedditAndReturnResponse("test", "test", "", "test")
            searchRedditAndReturnResponse("test", "test", "test", "")
            searchRedditAndReturnResponse(" ", "test", "test", "test")
            searchRedditAndReturnResponse("test", " ", "test", "test")
            searchRedditAndReturnResponse("test", "test", " ", "test")
            searchRedditAndReturnResponse("test", "test", "test", " ")

        # Test with None inputs
        with self.assertRaises(TypeError):
            searchRedditAndReturnResponse(None, None, None, None)

        # Test with numeric inputs
        with self.assertRaises(TypeError):
            searchRedditAndReturnResponse(123, 123, 123, 123)