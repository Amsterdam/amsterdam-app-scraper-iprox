""" Simple class file for stripping HTML tags from strings, with some magic for the Iprox web-pages """
import re
from bs4 import BeautifulSoup


class TextSanitizers:
    """ Reformat text (eg. strip html, capitalize, etc...)
    """
    @staticmethod
    def strip_html(html):
        """
        Strip all html tags from given string

        :param html: string
        :return: string
        """

        # Use BeautifulSoup to strip any html tags
        soup = BeautifulSoup(html, features='html.parser')
        text = soup.get_text(separator='\n\n', strip=True)

        # Cleanup text a bit
        regex_1 = re.compile('\.Zie ook')
        regex_2 = re.compile('â')
        regex_3 = re.compile('\b\.\b')
        text = re.sub(regex_1, '. Zie ook: ', text)
        text = re.sub(regex_2, '\'', text)
        text = re.sub(regex_3, '. ', text)
        return text

    @staticmethod
    def rewrite_html(html):
        """
        Rewrite specific strings in html

        :param html: string
        :return: string (html)
        """
        regex_1 = re.compile('"/publish/pages/')
        regex_2 = re.compile('<(?:(?!<).)*?>Klik op de \S+ om te vergroten.+?>')
        # regex_2 = re.compile('<figcapture>.+?>')

        html = re.sub(regex_1, '"https://www.amsterdam.nl/publish/pages/', html)
        html = re.sub(regex_2, '', html)
        return html

    @staticmethod
    def sentence_case(text, strip_spaces=True):
        """ Sentence case refers to titles in which only the first word has a capital letter, the same way a sentence
            is capitalized.
        """
        if strip_spaces is True:
            text = text.lstrip(' ').rstrip(' ')
            return str(text[0].upper() + text[1:])
        return str(text[0].upper() + text[1:])
