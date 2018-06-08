import spacy
import pytest

from spacy_readability import Readability


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
    assert 2 == read.num_sentences


def test_words(nlp, read):
    nlp.add_pipe(read, last=True)
    doc = nlp("I contain four words.")
    assert 4 == read.num_words


def test_syllables(nlp, read):
    nlp.add_pipe(read, last=True)
    doc = nlp("I contain four words.")
    assert 5 == read.num_syllables
