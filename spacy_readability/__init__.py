# coding: utf8
from spacy.tokens import Doc

from .about import __version__
from .words import word_list


class Readability(object):
    name = 'readability'

    def __init__(self, nlp):
        Doc.set_extension('flesch_kincaid_grade_level', getter=self.fk_grade)
        Doc.set_extension('flesch_kincaid_reading_ease', getter=self.fk_ease)
        Doc.set_extension('dale_chall', getter=self.dale_chall)

    def __call__(self, doc):
        self.num_sentences = len(list(doc.sents))
        self.num_words = self.get_num_words(doc)
        self.num_syllables = self.get_num_syllables(doc)
        return doc

    def fk_grade(self):
        return (11.8 * self.num_syllables / self.num_words) + (0.39 * self.num_words / self.num_sentences) - 15.59

    def fk_ease(self):
        return 206.835 - ((1.015 * self.num_words) / self.num_sentences) - ((84.6 * self.num_syllables) / self.num_words)

    def dale_chall(self, doc):
        diff_words_count = 0
        for word in doc:
            if word.text not in word_list:
                diff_words_count += 1

        percent_difficult_words = 100 * diff_words_count / self.num_words
        average_sentence_length = self.num_words / self.num_sentences
        grade = 0.1579 * percent_difficult_words + 0.0496 * average_sentence_length

        if percent_difficult_words > 5:
            grade += 3.6365
        return grade

    def get_num_words(self, doc):
        # filter spaces
        words_ = (w for w in doc if not w.is_space)

        # filter punctuation
        words_ = (w for w in words_ if not w.is_punct)
        return len(list(words_))

    def get_num_syllables(self, doc):
        # filter spaces
        words_ = (w for w in doc if not w.is_space)

        # filter punctuation
        words_ = (w for w in words_ if not w.is_punct)

        syllables_per_word = tuple(self.syllables(word) for word in words_)

        # set extension
        return sum(syllables_per_word)

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
