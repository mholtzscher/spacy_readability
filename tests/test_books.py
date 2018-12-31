import json
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


def validate_book(nlp, book):
    doc = nlp(book["text"])
    assert doc._.flesch_kincaid_grade_level == pytest.approx(book["fk_grade"], rel=1e-2)
    assert doc._.flesch_kincaid_reading_ease == pytest.approx(book["fk_ease"], rel=1e-2)
    assert doc._.coleman_liau_index == pytest.approx(book["coleman_liau"], rel=1e-2)
    assert doc._.automated_readability_index == pytest.approx(book["ari"], rel=1e-2)
    assert doc._.smog == pytest.approx(book["smog"], rel=1e-2)
    assert doc._.dale_chall == pytest.approx(book["dale_chall"], rel=1e-2)
    assert doc._.forcast == pytest.approx(book["forcast"], rel=1e-2)


def test_peter_rabbit(nlp):
    with open("tests/samples/peter_rabbit.json") as fp:
        data = json.load(fp)
    validate_book(nlp, data)


def test_tale_two_cities(nlp):
    with open("tests/samples/tale_of_two_cities.json") as fp:
        data = json.load(fp)
    validate_book(nlp, data)


@pytest.mark.parametrize(
    "text,expected",
    [
        (oliver_twist, 11.48),
        (secret_garden, 5.70),
        (flatland, 12.10),
        (grade_1, -1.52),
        (grade_2, 3.90),
        (grade_3, 2.42),
        (grade_4, 2.89),
        (grade_6, 3.45),
        (grade_8, 6.35),
        (grade_10, 7.41),
        (grade_12, 7.32),
        (grade_14, 11.58),
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
        (oliver_twist, 60.15),
        (secret_garden, 80.36),
        (flatland, 60.62),
        (grade_1, 115),
        (grade_2, 83.47),
        (grade_3, 93.38),
        (grade_4, 90.84),
        (grade_6, 92.02),
        (grade_8, 81.91),
        (grade_10, 69.60),
        (grade_12, 64.13),
        (grade_14, 54.12),
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
