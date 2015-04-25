# -*- coding: utf-8 -*-

from collections import defaultdict
from math import log


class WordDistribution(object):
    def __init__(self, tf=[], df=defaultdict(int)):
        self.tf = tf
        self.df = df
        self.tf_idf = []

    def update_dist(self, doc):
        self.update_tf(doc)
        self.update_df(doc)

    def update_tf(self, doc):
        word_dist = defaultdict(int)
        for word in doc:
            word_dist[word] += 1
        self.tf.append(word_dist)

    def update_df(self, doc):
        for word in set(doc):
            self.df[word] += 1

    def calc_tfidf(self, docs):
        N = len(docs)
        for doc, tf in zip(docs, self.tf):
            doc_tf_idf = {}
            for word in set(doc):
                doc_tf_idf[word] = tf[word] * log(float(N)/self.df[word])
            self.tf_idf.append(doc_tf_idf)

    def get_words_count_dist(self):
        word_counts = defaultdict(int)
        for tf in self.tf:
            for word in tf:
                word_counts[word] += 1
        return word_counts

    def show_result(self):
        totla_word_dist = self.get_words_count_dist()
        print "==== total word counts ===="
        for word, count in sorted(totla_word_dist.items(), key=lambda x: x[1], reverse=True)[:20]:
            print "{}: {}".format(word.encode('utf-8'), count)

if __name__ == '__main__':
    docs = [[u'明日', u'天気', u'晴れ'],
            [u'昨日', u'天気', u'雨'],
            [u'明日', u'明後日', u'雨'],
            ]
    N = len(docs)
    word_dist = WordDistribution()

    for doc in docs:
        word_dist.update_dist(doc)
    word_dist.calc_tfidf(docs)

    print "==== TF ===="
    for doc_i, tf in enumerate(word_dist.tf):
        print "==== doc{}  ====".format(doc_i+1)
        for word in tf:
            print "{}: {}".format(word.encode('utf-8'), tf[word])

    print "==== DF ===="
    for word in word_dist.df:
        print "{}: {}".format(word.encode('utf-8'), word_dist.df[word])

    print "==== IDF ===="
    for word in word_dist.df:
        print "{}: {}".format(word.encode('utf-8'), log(float(N)/word_dist.df[word]))

    print "==== TFIDF ===="
    for doc_i, doc_tf_idf in enumerate(word_dist.tf_idf):
        print "==== doc{}  ====".format(doc_i+1)
        for word in doc_tf_idf:
            print "{}: {}".format(word.encode('utf-8'), doc_tf_idf[word])

    print "==== total word counts ===="
    for word, count in word_dist.get_words_count_dist().items():
        print "{}: {}".format(word.encode('utf-8'), count)