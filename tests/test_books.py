import spacy
import pytest

from spacy_readability import Readability
from .books import oliver_twist, secret_garden, flatland

textacy_corpus = """
Mr. Speaker, 480,000 Federal employees are working without pay, a form of involuntary servitude; 280,000 Federal employees are not working, and they will be paid. Virtually all of these workers have mortgages to pay, children to feed, and financial obligations to meet.
Mr. Speaker, what is happening to these workers is immoral, is wrong, and must be rectified immediately. Newt Gingrich and the Republican leadership must not continue to hold the House and the American people hostage while they push their disastrous 7-year balanced budget plan. The gentleman from Georgia, Mr. Gingrich, and the Republican leadership must join Senator Dole and the entire Senate and pass a continuing resolution now, now to reopen Government.
Mr. Speaker, that is what the American people want, that is what they need, and that is what this body must do.
"""


@pytest.fixture(scope='module')
def nlp():
    pipeline = spacy.load('en')
    pipeline.add_pipe(Readability())
    return pipeline


@pytest.mark.parametrize("text,expected", [
    (oliver_twist, 11.64),
    (secret_garden, 6.00),
    (flatland, 13.51),
    (textacy_corpus, 12.30)
])
def test_flesch_kincaid_grade_level(text, expected, nlp):
    doc = nlp(text)
    assert doc._.flesch_kincaid_grade_level == pytest.approx(expected, rel=1e-2)


@pytest.mark.parametrize("text,expected", [
    (oliver_twist, 60.94),
    (secret_garden, 80.49),
    (flatland, 58.11),
    (textacy_corpus, 48.39)
])
def test_flesch_kincaid_reading_ease(text, expected, nlp):
    doc = nlp(text)
    assert doc._.flesch_kincaid_reading_ease == pytest.approx(expected, rel=1e-2)


@pytest.mark.parametrize("text,expected", [
    (oliver_twist, 9.72),
    (secret_garden, 8.49),
    (flatland, 9.48),
    (textacy_corpus, 10.54)
])
def test_dale_chall(text, expected, nlp):
    doc = nlp(text)
    assert doc._.dale_chall == pytest.approx(expected, rel=1e-2)


@pytest.mark.parametrize("text,expected", [
    (oliver_twist, 19.89),
    (secret_garden, 13.06),
    (flatland, 0),
    (textacy_corpus, 0)
])
def test_smog(text, expected, nlp):
    doc = nlp(text)
    assert expected == pytest.approx(doc._.smog, rel=1e-2)


@pytest.mark.parametrize("text,expected", [
    (oliver_twist, 7.14),
    (secret_garden, 4.65),
    (flatland, 6.26),
    (textacy_corpus, 11.86)
])
def test_coleman_liau(text, expected, nlp):
    doc = nlp(text)
    assert expected == pytest.approx(doc._.coleman_liau_index, rel=1e-2)


@pytest.mark.parametrize("text,expected", [
    (oliver_twist, 11.64),
    (secret_garden, 4.43),
    (flatland, 13.8),
    (textacy_corpus, 13.41)
])
def test_ari(text, expected, nlp):
    doc = nlp(text)
    assert expected == pytest.approx(doc._.automated_readability_index, rel=1e-2)
