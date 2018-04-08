import spacy
import pytest

from spacy_readability import Readability


@pytest.fixture(scope='function')
def nlp():
    return spacy.load('en')


def test_simple(nlp):
    doc = nlp("sample")
    assert doc


def test_integration(nlp):
    read = Readability(nlp)
    nlp.add_pipe(read, last=True)
    assert nlp.pipe_names[-1] == 'readability'


def test_sentences(nlp):
    read = Readability(nlp)
    nlp.add_pipe(read, last=True)
    doc = nlp("I am 2 sents. I am the best panda?")
    assert read.num_sentences == 2

