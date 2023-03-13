""" UNITTEST """
import unittest
from GenericFunctions.TextSanitizers import TextSanitizers


class Unittests(unittest.TestCase):
    """ Unittests """
    @staticmethod
    def test_strip_html():
        """ Strip html tags from data """
        html = '<div>mock data</div>'
        text_sanitizer = TextSanitizers()
        result = text_sanitizer.strip_html(html)

        assert result == 'mock data'

    @staticmethod
    def test_sentence_case_strip_spaces():
        """ Test strip spaces from text and capitalize first letter """
        sentence = ' mock '
        text_sanitizer = TextSanitizers()
        result = text_sanitizer.sentence_case(sentence, strip_spaces=True)

        assert result == 'Mock'

    @staticmethod
    def test_sentence_case_do_not_strip_spaces():
        """ Test don't strip spaces from text and capitalize first letter """
        sentence = ' mock '
        text_sanitizer = TextSanitizers()
        result = text_sanitizer.sentence_case(sentence, strip_spaces=False)

        assert result == ' mock '
