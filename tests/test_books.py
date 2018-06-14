import spacy
import pytest
import ftfy

from spacy_readability import Readability
from .books import *


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
        (grade_1, -1.52),
        (grade_2, 3.77),
        (grade_3, 2.5),
        (grade_4, 2.89),
        (grade_6, 3.59),
        (grade_8, 6.67),
        (grade_10, 7.58),
        (grade_12, 7.44),
        (grade_14, 11.75),
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
        (grade_1, 115),
        (grade_2, 84.39),
        (grade_3, 93.38),
        (grade_4, 90.84),
        (grade_6, 91.03),
        (grade_8, 79.59),
        (grade_10, 68.35),
        (grade_12, 63.26),
        (grade_14, 52.93),
    ],
)
def test_flesch_kincaid_reading_ease(text, expected, nlp):
    text = ftfy.fix_text(text)
    text = " ".join(text.split())
    doc = nlp(text)
    assert pytest.approx(expected, rel=1e-2) == doc._.flesch_kincaid_reading_ease


@pytest.mark.parametrize(
    "text,expected", [(oliver_twist, 7.64), (secret_garden, 5.83), (flatland, 7.07)]
)
def test_dale_chall(text, expected, nlp):
    text = ftfy.fix_text(text)
    text = " ".join(text.split())
    doc = nlp(text)
    assert pytest.approx(expected, rel=1e-2) == doc._.dale_chall


@pytest.mark.parametrize(
    "text,expected", [(oliver_twist, 19.76), (secret_garden, 12.84), (flatland, 0)]
)
def test_smog(text, expected, nlp):
    text = ftfy.fix_text(text)
    text = " ".join(text.split())
    doc = nlp(text)
    assert pytest.approx(expected, rel=1e-2) == doc._.smog


@pytest.mark.parametrize(
    "text,expected", [(oliver_twist, 8.85), (secret_garden, 6.38), (flatland, 7.76)]
)
def test_coleman_liau(text, expected, nlp):
    text = ftfy.fix_text(text)
    text = " ".join(text.split())
    doc = nlp(text)
    assert pytest.approx(expected, rel=1e-2) == doc._.coleman_liau_index


@pytest.mark.parametrize(
    "text,expected", [(oliver_twist, 12.37), (secret_garden, 5.30), (flatland, 12.97)]
)
def test_ari(text, expected, nlp):
    text = ftfy.fix_text(text)
    text = " ".join(text.split())
    doc = nlp(text)
    assert pytest.approx(expected, rel=1e-2) == doc._.automated_readability_index


@pytest.mark.parametrize(
    "text,expected", [(oliver_twist, 10.7), (secret_garden, 10.2), (flatland, 11.8)]
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
