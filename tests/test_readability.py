from spacy.lang.en import English
import pytest

from spacy_readability import Readability

@pytest.fixture(scope='function')
def nlp():
    return English()

def test_simple(nlp):
    assert True