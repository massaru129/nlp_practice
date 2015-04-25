# -*- coding: utf-8 -*-

__author__ = 'masaru'

import unicodedata
import igo

tagger = igo.tagger.Tagger('dict/neologd')


class SentenceParser():
    tagger = tagger

    def __init__(self, sentence):
        self.nodes = None
        # if not isinstance(sentence, unicode):
        #     sentence = sentence.decode('utf-8')
        # self.sentence = unicodedata.normalize('NFKC', sentence)
        self.sentence = sentence

    def parse(self):
        self.nodes = self.tagger.parse(self.sentence)

    def extract_words(self):
        words = []
        for node in self.nodes:
            words.append(node.surface)
        return words

    def extract_nouns(self):
        if self.nodes is None:
            self.parse()
        nouns = []
        for node in self.nodes:
            if node.feature.split(',')[0] == u'名詞' and len(node.surface) > 1:
                nouns.append(node.surface)
        return nouns