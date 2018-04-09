#spacy-readability
**************************
[![Build Status](https://travis-ci.org/mholtzscher/spacy_readability.svg?branch=master)](https://travis-ci.org/mholtzscher/spacy_readability)
[![PyPI version](https://badge.fury.io/py/spacy-readability.svg)](https://badge.fury.io/py/spacy-readability)

spaCy v2.0 pipeline component for calculating readability scores of of text. Provides scores for Flesh-Kincaid grade level, Flesh-Kincaid reading ease, and Dale-Chall.

## Installation

```
pip install spacy-readability
```

## Usage    
    
```python
import spacy
from spacy_readability import Readability

nlp = spacy.load('en')
read = Readability(nlp)
nlp.add_pipe(read, last=True)
doc = nlp("I am some really difficult text to read because I use obnoxiously large words.")
doc._.flesch_kincaid_grade_level
doc._.flesch_kincaid_reading_ease
doc._.dale_chall
```
