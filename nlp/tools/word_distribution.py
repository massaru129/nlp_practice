# -*- coding: utf-8 -*-

from collections import defaultdict
from math import log


class WordDistribution(object):
    def __init__(self):
        self.tf = []
        self.df = defaultdict(int)
        self.tf_idf = []
        self.total_words_dist = defaultdict(int)

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
        if len(docs) != len(self.tf):
            print "number of docs is different from the calculated term frequency"
            return False
        for doc, tf in zip(docs, self.tf):
            doc_tf_idf = {}
            for word in set(doc):
                doc_tf_idf[word] = tf[word] * log(float(N)/self.df[word])
            self.tf_idf.append(doc_tf_idf)
        return True

    def calc_total_words_dist(self):
        for tf in self.tf:
            for word in tf:
                self.total_words_dist[word] += 1

    def extract_top_n_percent_words(self, n=1):
        """
        出現頻度が上位nパーセントの単語を計算済みの単語分布から削除する
        :param n:
        :return:
        """
        percentage = float(n)/100
        remove_word_count = int(percentage * self.total_words_count)
        sorted_words_dist = sorted(self.total_words_dist.items(), key=lambda x: x[1], reverse=True)
        remove_words = []
        for word, count in sorted_words_dist:
            if count > remove_word_count:
                remove_words.append(word)
            else:
                break
        return remove_words

    def remove_words(self, words):
        for word in words:
            if word not in self.df:
                continue
            del self.total_words_dist[word]
            del self.df[word]
            for doc_i in xrange(len(self.tf)):
                if word not in self.tf[doc_i]:
                    continue
                del self.tf[doc_i][word]

    @property
    def total_words_count(self):
        return sum(self.total_words_dist.values())

    def show_result(self, remove_stopword=False):
        print "==== total word counts ===="
        if remove_stopword:
            tf = self.remove_top_n_percent_words()
        else:
            tf = self.total_words_dist
        for word, count in tf:
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