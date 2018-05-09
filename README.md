# spacy-readability
**************************
[![Build Status](https://travis-ci.org/mholtzscher/spacy_readability.svg?branch=master)](https://travis-ci.org/mholtzscher/spacy_readability)
[![PyPI version](https://badge.fury.io/py/spacy-readability.svg)](https://badge.fury.io/py/spacy-readability)

spaCy v2.0 pipeline component for calculating readability scores of of text. Provides scores for Flesh-Kincaid grade level, Flesh-Kincaid reading ease, Dale-Chall, and SMOG.

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

print(doc._.flesch_kincaid_grade_level)
print(doc._.flesch_kincaid_reading_ease)
print(doc._.dale_chall)
print(doc._.smog)
print(doc._.coleman_liau_index)
print(doc._.automated_readability_index)
```

## Readability Scores

Readability is the ease with which a reader can understand a written text. In natural language, the readability of text depends on its content (the complexity of its vocabulary and syntax) and its presentation (such as typographic aspects like font size, line height, and line length).

### Popular Metrics
* The Flesch formulas
  * Flesch-Kincaid Readability Score
  * Flesch-Kincaid Reading Ease
* Dale-Chall formula
* SMOG
* Coleman-Liau Index

[For more in depth reading.](https://en.wikipedia.org/wiki/Readability)
