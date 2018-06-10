import spacy
import pytest
import ftfy

from spacy_readability import Readability
from .books import oliver_twist, secret_garden, flatland

textacy_corpus = """
Mr. Speaker, 480,000 Federal employees are working without pay, a form of involuntary servitude; 280,000 Federal employees are not working, and they will be paid. Virtually all of these workers have mortgages to pay, children to feed, and financial obligations to meet.
Mr. Speaker, what is happening to these workers is immoral, is wrong, and must be rectified immediately. Newt Gingrich and the Republican leadership must not continue to hold the House and the American people hostage while they push their disastrous 7-year balanced budget plan. The gentleman from Georgia, Mr. Gingrich, and the Republican leadership must join Senator Dole and the entire Senate and pass a continuing resolution now, now to reopen Government.
Mr. Speaker, that is what the American people want, that is what they need, and that is what this body must do.
"""


@pytest.fixture(scope="module")
def nlp():
    pipeline = spacy.load("en")
    pipeline.add_pipe(Readability())
    return pipeline


@pytest.mark.parametrize(
    "text,expected",
    [
        (oliver_twist, 11.48),
        (secret_garden, 5.84),
        (flatland, 12.26),
        (textacy_corpus, 12.30),
    ],
)
def test_flesch_kincaid_grade_level(text, expected, nlp):
    text = ftfy.fix_text(text)
    text = " ".join(text.split())
    doc = nlp(text)
    assert pytest.approx(expected, rel=1e-2) == doc._.flesch_kincaid_grade_level


@pytest.mark.parametrize(
    "text,expected",
    [
        (oliver_twist, 59.54),
        (secret_garden, 78.72),
        (flatland, 59.47),
        (textacy_corpus, 46.97),
    ],
)
def test_flesch_kincaid_reading_ease(text, expected, nlp):
    text = ftfy.fix_text(text)
    text = " ".join(text.split())
    doc = nlp(text)
    assert pytest.approx(expected, rel=1e-2) == doc._.flesch_kincaid_reading_ease


@pytest.mark.parametrize(
    "text,expected",
    [
        (oliver_twist, 7.64),
        (secret_garden, 5.83),
        (flatland, 7.07),
        (textacy_corpus, 9.63),
    ],
)
def test_dale_chall(text, expected, nlp):
    text = ftfy.fix_text(text)
    text = " ".join(text.split())
    doc = nlp(text)
    assert pytest.approx(expected, rel=1e-2) == doc._.dale_chall


@pytest.mark.parametrize(
    "text,expected",
    [(oliver_twist, 19.76), (secret_garden, 12.84), (flatland, 0), (textacy_corpus, 0)],
)
def test_smog(text, expected, nlp):
    text = ftfy.fix_text(text)
    text = " ".join(text.split())
    doc = nlp(text)
    assert pytest.approx(expected, rel=1e-2) == doc._.smog


@pytest.mark.parametrize(
    "text,expected",
    [
        (oliver_twist, 8.85),
        (secret_garden, 6.38),
        (flatland, 7.76),
        (textacy_corpus, 12.51),
    ],
)
def test_coleman_liau(text, expected, nlp):
    text = ftfy.fix_text(text)
    text = " ".join(text.split())
    doc = nlp(text)
    assert pytest.approx(expected, rel=1e-2) == doc._.coleman_liau_index


@pytest.mark.parametrize(
    "text,expected",
    [
        (oliver_twist, 12.37),
        (secret_garden, 5.30),
        (flatland, 12.97),
        (textacy_corpus, 13.62),
    ],
)
def test_ari(text, expected, nlp):
    text = ftfy.fix_text(text)
    text = " ".join(text.split())
    doc = nlp(text)
    assert pytest.approx(expected, rel=1e-2) == doc._.automated_readability_index


@pytest.mark.parametrize(
    "text,expected",
    [
        (oliver_twist, 10.7),
        (secret_garden, 10.2),
        (flatland, 11.8),
        (textacy_corpus, 0),
    ],
)
def test_forcast(text, expected, nlp):
    text = ftfy.fix_text(text)
    text = " ".join(text.split())
    doc = nlp(text)
    assert pytest.approx(expected, rel=1e-2) == doc._.forcast


@pytest.mark.parametrize(
    "text,expected",
    [
        (oliver_twist, 0.357),
        (secret_garden, -0.56),
        (flatland, 1.24),
        (textacy_corpus, 11.16),
    ],
)
def test_linsear_write(text, expected, nlp):
    text = ftfy.fix_text(text)
    text = " ".join(text.split())
    doc = nlp(text)
    assert pytest.approx(expected, rel=1e-2) == doc._.linsear_write
