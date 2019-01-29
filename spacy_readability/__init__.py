# -*- coding: utf-8 -*-

"""Top-level package for spacy_readability."""

__author__ = """Michael Holtzscher"""
__email__ = "mholtz@protonmail.com"
__version__ = "1.4.1"

from math import sqrt
from spacy.tokens import Doc
import syllapy

from .words import DALE_CHALL_WORDS


class Readability:
    """spaCy v2.0 pipeline component for calculating readability scores of of text.
    Provides scores for Flesh-Kincaid grade level, Flesh-Kincaid reading ease, and Dale-Chall.
    USAGE:
        >>> import spacy
        >>> from spacy_readability import Readability
        >>> nlp = spacy.load('en')
        >>> read = Readability()
        >>> nlp.add_pipe(read, last=True)
        >>> doc = nlp("I am some really difficult text. I use obnoxiously large words.")
        >>> print(doc._.flesch_kincaid_grade_level)
        >>> print(doc._.flesch_kincaid_reading_ease)
        >>> print(doc._.dale_chall)
        >>> print(doc._.smog)
        >>> print(doc._.coleman_liau_index)
        >>> print(doc._.automated_readability_index)
        >>> print(doc._.forcast)
    """

    name = "readability"

    def __init__(self):
        """Initialise the pipeline component.
        """
        if not Doc.has_extension("flesch_kincaid_grade_level"):
            Doc.set_extension("flesch_kincaid_grade_level", getter=self.fk_grade)

        if not Doc.has_extension("flesch_kincaid_reading_ease"):
            Doc.set_extension("flesch_kincaid_reading_ease", getter=self.fk_ease)

        if not Doc.has_extension("dale_chall"):
            Doc.set_extension("dale_chall", getter=self.dale_chall)

        if not Doc.has_extension("smog"):
            Doc.set_extension("smog", getter=self.smog)

        if not Doc.has_extension("coleman_liau_index"):
            Doc.set_extension("coleman_liau_index", getter=self.coleman_liau)

        if not Doc.has_extension("automated_readability_index"):
            Doc.set_extension("automated_readability_index", getter=self.ari)

        if not Doc.has_extension("forcast"):
            Doc.set_extension("forcast", getter=self.forcast)

    def __call__(self, doc):
        """Apply the pipeline component to a `Doc` object.
        doc (Doc): The `Doc` returned by the previous pipeline component.
        RETURNS (Doc): The modified `Doc` object.
        """
        return doc

    def fk_grade(self, doc):
        """Returns the Flesch-Kincaid grade for the document.
        """
        num_sentences = _get_num_sentences(doc)
        num_words = _get_num_words(doc)
        num_syllables = _get_num_syllables(doc)
        if num_sentences == 0 or num_words == 0 or num_syllables == 0:
            return 0
        return (
            (11.8 * num_syllables / num_words)
            + (0.39 * num_words / num_sentences)
            - 15.59
        )

    def fk_ease(self, doc):
        """Returns the Flesch-Kincaid Reading Ease score for the document.
        """
        num_sentences = _get_num_sentences(doc)
        num_words = _get_num_words(doc)
        num_syllables = _get_num_syllables(doc)
        if num_sentences == 0 or num_words == 0 or num_syllables == 0:
            return 0
        words_per_sent = num_words / num_sentences
        syllables_per_word = num_syllables / num_words
        return 206.835 - (1.015 * words_per_sent) - (84.6 * syllables_per_word)

    def dale_chall(self, doc):
        """Returns the Dale-Chall score for the document.
        """
        num_sentences = _get_num_sentences(doc)
        num_words = _get_num_words(doc)
        if num_sentences == 0 or num_words == 0:
            return 0

        diff_words_count = 0
        for word in doc:
            if not word.is_punct and "'" not in word.text:
                if (
                    word.text.lower() not in DALE_CHALL_WORDS
                    and word.lemma_.lower() not in DALE_CHALL_WORDS
                ):
                    diff_words_count += 1

        percent_difficult_words = 100 * diff_words_count / num_words
        average_sentence_length = num_words / num_sentences
        grade = 0.1579 * percent_difficult_words + 0.0496 * average_sentence_length

        # if percent difficult words is about 5% then adjust score
        if percent_difficult_words > 5:
            grade += 3.6365
        return grade

    def smog(self, doc):
        """Returns the SMOG score for the document. If there are less than 30 sentences then
        it returns 0 because he formula significantly loses accuracy on small corpora.
        """
        num_sentences = _get_num_sentences(doc)
        num_words = _get_num_words(doc)
        if num_sentences < 30 or num_words == 0:
            return 0
        num_poly = _get_num_syllables(doc, min_syllables=3)
        return 1.0430 * sqrt(num_poly * 30 / num_sentences) + 3.1291

    def coleman_liau(self, doc):
        """Returns the Coleman-Liau index for the document."""
        num_words = _get_num_words(doc)
        if num_words <= 0:
            return 0

        num_sentences = _get_num_sentences(doc)
        letter_count = sum(
            [len(token) for token in doc if not token.is_punct and not token.is_digit]
        )
        if letter_count <= 0:
            return 0
        letters_to_words = letter_count / num_words * 100
        sent_to_words = num_sentences / num_words * 100
        return 0.0588 * letters_to_words - 0.296 * sent_to_words - 15.8

    def ari(self, doc):
        """Returns the Automated Readability Index for the document."""
        num_sentences = _get_num_sentences(doc)
        num_words = _get_num_words(doc)
        if num_words <= 0:
            return 0

        letter_count = sum([len(token) for token in doc if not token.is_punct])
        letter_to_words = letter_count / num_words
        words_to_sents = num_words / num_sentences
        return 4.71 * letter_to_words + 0.5 * words_to_sents - 21.43

    def forcast(self, doc):
        """Returns the Forcast score for the document.
        """
        num_words = _get_num_words(doc)

        if num_words < 150:
            return 0

        mono_syllabic = 0
        for i in range(150):
            if syllapy.count(doc[i].text) == 1:
                mono_syllabic += 1
        return 20 - (mono_syllabic / 10)


def _get_num_sentences(doc: Doc):
    """Return number of sentences in the document
    """
    return len(list(doc.sents))


def _get_num_words(doc: Doc):
    """Return number of words in the document.
    Filters punctuation and words that start with apostrophe (aka contractions)
    """
    filtered_words = [
        word for word in doc if not word.is_punct and "'" not in word.text
    ]
    return len(filtered_words)


def _get_num_syllables(doc: Doc, min_syllables: int = 1):
    """Return number of words in the document.
    Filters punctuation and words that start with apostrophe (aka contractions)
    """
    text = (word for word in doc if not word.is_punct and "'" not in word.text)
    syllables_per_word = tuple(syllapy.count(word.text) for word in text)
    return sum(c for c in syllables_per_word if c >= min_syllables)
