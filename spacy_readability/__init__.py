# coding: utf8
from math import sqrt

from spacy.tokens import Doc

from .words import word_list


class Readability(object):
    """spaCy v2.0 pipeline component for calculating readability scores of of text. Provides scores for
    Flesh-Kincaid grade level, Flesh-Kincaid reading ease, and Dale-Chall.
    USAGE:
        >>> import spacy
        >>> from spacy_readability import Readability
        >>> nlp = spacy.load('en')
        >>> read = Readability()
        >>> nlp.add_pipe(read, last=True)
        >>> doc = nlp("I am some really difficult text to read because I use obnoxiously large words.")
        >>> print(doc._.flesch_kincaid_grade_level)
        >>> print(doc._.flesch_kincaid_reading_ease)
        >>> print(doc._.dale_chall)
        >>> print(doc._.smog)
        >>> print(doc._.coleman_liau_index)
        >>> print(doc._.automated_readability_index)
    """

    name = 'readability'

    def __init__(self):
        """Initialise the pipeline component.
        """
        if not Doc.has_extension('flesch_kincaid_grade_level'):
            Doc.set_extension('flesch_kincaid_grade_level', getter=self.fk_grade)

        if not Doc.has_extension('flesch_kincaid_reading_ease'):
            Doc.set_extension('flesch_kincaid_reading_ease', getter=self.fk_ease)

        if not Doc.has_extension('dale_chall'):
            Doc.set_extension('dale_chall', getter=self.dale_chall)

        if not Doc.has_extension('smog'):
            Doc.set_extension('smog', getter=self.smog)

        if not Doc.has_extension('coleman_liau_index'):
            Doc.set_extension('coleman_liau_index', getter=self.coleman_liau)

        if not Doc.has_extension('automated_readability_index'):
            Doc.set_extension('automated_readability_index', getter=self.ari)

    def __call__(self, doc):
        """Apply the pipeline component to a `Doc` object.
        doc (Doc): The `Doc` returned by the previous pipeline component.
        RETURNS (Doc): The modified `Doc` object.
        """
        self.num_sentences = len(list(doc.sents))
        self.num_words = self.get_num_words(doc)
        self.num_syllables = self.get_num_syllables(doc)
        return doc

    def fk_grade(self, doc):
        if self.num_sentences == 0 or self.num_words == 0 or self.num_syllables == 0:
            return 0
        return (11.8 * self.num_syllables / self.num_words) + (0.39 * self.num_words / self.num_sentences) - 15.59

    def fk_ease(self, doc):
        if self.num_sentences == 0 or self.num_words == 0 or self.num_syllables == 0:
            return 0
        return 206.835 - ((1.015 * self.num_words) / self.num_sentences) - (
                (84.6 * self.num_syllables) / self.num_words)

    def dale_chall(self, doc):
        if self.num_sentences == 0 or self.num_words == 0:
            return 0

        diff_words_count = 0
        for word in doc:
            if not word.is_punct and "'" not in word.text:
                if word.text.lower() not in word_list:
                    diff_words_count += 1

        percent_difficult_words = 100 * diff_words_count / self.num_words
        average_sentence_length = self.num_words / self.num_sentences
        grade = 0.1579 * percent_difficult_words + 0.0496 * average_sentence_length

        # if percent difficult words is about 5% then adjust score
        if percent_difficult_words > 5:
            grade += 3.6365
        return grade

    def smog(self, doc):
        """Returns the SMOG score for the document. If there are less than 30 sentences then
        it returns 0 because he formula significantly loses accuracy on small corpora.
        """
        if self.num_sentences < 30 or self.num_words == 0:
            return 0

        num_poly = self.get_num_syllables(doc, min_syllables=3)
        return 1.0430 * sqrt(num_poly * 30 / self.num_sentences) + 3.1291

    def coleman_liau(self, doc):
        """Returns the Coleman-Liau index for the document."""
        letter_count = sum([len(token) for token in doc if not token.is_punct and not token.is_digit])
        letters_to_words = letter_count / self.num_words * 100
        sent_to_words = self.num_sentences / self.num_words * 100
        return 0.0588 * letters_to_words - 0.296 * sent_to_words - 15.8

    def ari(self, doc):
        """Returns the Automated Readability Index for the document."""
        letter_count = sum([len(token) for token in doc if not token.is_punct])
        return 4.71 * (letter_count / self.num_words) + 0.5 * (self.num_words / self.num_sentences) - 21.43

    def get_num_words(self, doc):
        # filter punctuation and words that start with apostrophe (aka contractions)
        words_ = (word for word in doc if not word.is_punct and "'" not in word.text)
        return len(list(words_))

    def get_num_syllables(self, doc, min_syllables=1):
        # filter punctuation and words that start with apostrophe (aka contractions)
        text = (word for word in doc if not word.is_punct and "'" not in word.text)
        syllables_per_word = tuple(self.syllables(word) for word in text)
        return sum(c for c in syllables_per_word if c >= min_syllables)

    def syllables(self, token):
        count = 0
        vowels = 'aeiouy'
        word = token.text.lower().strip(".:;?!")
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith('e'):
            count -= 1
        if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
            count += 1
        if count == 0:
            count += 1
        return count
