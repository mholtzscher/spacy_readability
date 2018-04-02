from spacy.lang.en import English
import pytest

from spacy_readability import Readability


@pytest.fixture(scope='function')
def nlp():
    return English()


def test_simple(nlp):
    doc = nlp("sample")
    assert doc


def test_integration(nlp):
    read = Readability(nlp)
    nlp.add_pipe(read, last=True)
    assert nlp.pipe_names[-1] == 'readability'
