from GenericFunctions.TextSanitizers import TextSanitizers


def test_strip_html():
    html = '<div>mock data</div>'
    text_sanitizer = TextSanitizers()
    result = text_sanitizer.strip_html(html)

    assert result == 'mock data'


def test_sentence_case_strip_spaces():
    sentence = ' mock '
    text_sanitizer = TextSanitizers()
    result = text_sanitizer.sentence_case(sentence, strip_spaces=True)

    assert result == 'Mock'


def test_sentence_case_do_not_strip_spaces():
    sentence = ' mock '
    text_sanitizer = TextSanitizers()
    result = text_sanitizer.sentence_case(sentence, strip_spaces=False)

    assert result == ' mock '
