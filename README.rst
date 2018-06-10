=================
spacy_readability
=================


.. image:: https://img.shields.io/pypi/v/spacy_readability.svg
        :target: https://pypi.python.org/pypi/spacy_readability

.. image:: https://img.shields.io/travis/mholtzscher/spacy_readability.svg
        :target: https://travis-ci.org/mholtzscher/spacy_readability

.. image:: https://readthedocs.org/projects/spacy-readability/badge/?version=latest
        :target: https://spacy-readability.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/mholtzscher/spacy_readability/shield.svg
     :target: https://pyup.io/repos/github/mholtzscher/spacy_readability/
     :alt: Updates



spaCy v2.0 pipeline component for calculating readability scores of of text. Provides scores for Flesh-Kincaid grade level, Flesh-Kincaid reading ease, Dale-Chall, and SMOG.

* Free software: MIT license
* Documentation: https://spacy-readability.readthedocs.io.

************
Installation
************

.. code-block:: python

    pip install spacy-readability

*****
Usage
*****

.. code-block:: python

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
    print(doc._.forcast)
    print(doc._.linsear_write)

Readability Scores
******************

Readability is the ease with which a reader can understand a written text. In natural language, the readability of text depends on its content (the complexity of its vocabulary and syntax) and its presentation (such as typographic aspects like font size, line height, and line length).

Popular Metrics
---------------
- The Flesch formulas
   - Flesch-Kincaid Readability Score
   - Flesch-Kincaid Reading Ease
- Dale-Chall formula
- SMOG
- Coleman-Liau Index
- Automated Readability Index
- FORCAST
- Linsear Write

`For more in depth reading. <https://en.wikipedia.org/wiki/Readability>`_

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
