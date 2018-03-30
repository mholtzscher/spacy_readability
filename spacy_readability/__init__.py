# coding: utf8
from spacy.tokens import Doc, Span, Token

from .about import __version__


class Readability(object):
    name = 'readability'

    def __init__(self, nlp):
        Doc.set_extension('flesch_kincaid_grade_level', getter=self.fk_grade)
        Doc.set_extension('flesch_kincaid_ease', getter=self.fk_ease)
        Doc.set_extension('dale_chall', default=0)

    def __call__(self, doc):
        self.num_sents = len(list(doc.sents))
        self.num_words = self.getNumWords(doc)
        self.num_syllables = self.getNumSyllables(doc)
        return doc
    
    def fk_grade(self, doc):
         return (11.8 * self.num_syllables / self.num_words) + (0.39 * self.num_words / self.num_sents) - 15.59
        
    def fk_ease(self, doc):
        return 206.835 - ((1.015 * self.num_words) / self.num_sents) - ((84.6 * self.num_syllables) / self.num_words)
    
    def dale_chall(self, doc):
        return 0
    
    def getNumWords(self, doc):
        # filter spaces
        words_ = (w for w in doc if not w.is_space)
    
        # filter punctuation
        words_ = (w for w in words_ if not w.is_punct)
        return len(list(words_))
    
    def getNumSyllables(self, doc):
         # filter spaces
        words = (w for w in doc if not w.is_space)
        
        # filter punctuation
        words = (w for w in words if not w.is_punct)
        
        syllables_per_word = tuple(self.syllables(word) for word in words)
        
        # set extension
        return sum(syllables_per_word)
    
    def syllables(self, token):
        count = 0
        vowels = 'aeiouy'
        word = token.text.lower().strip(".:;?!")
        if word[0] in vowels:
            count +=1
        for index in range(1,len(word)):
            if word[index] in vowels and word[index-1] not in vowels:
                count +=1
        if word.endswith('e'):
            count -= 1
        if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
            count+=1
        if count == 0:
            count +=1
        return count
        
        