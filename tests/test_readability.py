import spacy
import pytest

from spacy.tokens import Doc
from spacy_readability import (
    Readability,
    _get_num_sentences,
    _get_num_syllables,
    _get_num_words,
)


@pytest.fixture(scope="function")
def nlp():
    return spacy.load("en")


@pytest.fixture(scope="function")
def read():
    return Readability()


def test_simple(nlp):
    doc = nlp("sample")
    assert doc


def test_integration(nlp, read):
    nlp.add_pipe(read, last=True)
    assert "readability" == nlp.pipe_names[-1]


def test_sentences(nlp, read):
    nlp.add_pipe(read, last=True)
    doc = nlp("I am 2 sentences. I am the best panda?")
    assert 2 == _get_num_sentences(doc)


def test_words(nlp, read):
    nlp.add_pipe(read, last=True)
    doc = nlp("I contain four words.")
    assert 4 == _get_num_words(doc)


def test_syllables(nlp, read):
    nlp.add_pipe(read, last=True)
    doc = nlp("I contain four words.")
    assert 5 == _get_num_syllables(doc)


def test_extensions(nlp, read):
    nlp.add_pipe(read, last=True)
    doc = nlp("I contain four words.")
    assert Doc.has_extension("flesch_kincaid_grade_level")
    assert Doc.has_extension("flesch_kincaid_reading_ease")
    assert Doc.has_extension("dale_chall")
    assert Doc.has_extension("smog")
    assert Doc.has_extension("coleman_liau_index")
    assert Doc.has_extension("automated_readability_index")
    assert Doc.has_extension("forcast")


@pytest.mark.parametrize("text,expected", [("", 0), ("#", 0)])
def test_edge_scenarios(text, expected, nlp, read):
    nlp.add_pipe(read, last=True)
    doc = nlp(text)
    assert doc._.flesch_kincaid_grade_level == expected
    assert doc._.flesch_kincaid_reading_ease == expected
    assert doc._.coleman_liau_index == expected
    assert doc._.automated_readability_index == expected
    assert doc._.smog == expected
    assert doc._.dale_chall == expected
    assert doc._.forcast == expected
