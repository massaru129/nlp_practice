# -*- coding: utf-8 -*-
__author__ = 'masaru'

import sys
sys.path.append('..')
from db.mongodb import MongoDB
from tools.parser import SentenceParser
from utils.pickle_tool import dump_object
from tools.word_distribution import WordDistribution


def calc_words_dist():
    mongo = MongoDB(host='localhost', port=27017, db_name='mery')
    mongo.load_database()
    articles = mongo.load_collection('articles')
    word_distributions = {}
    categories = [u"ファッション", u"メイク・コスメ", u"ヘアスタイル", u"ネイル", u"美容",
                  u"グルメ", u"旅行・おでかけ", u"恋愛", u"ライフスタイル", ]
    total_words_dist = WordDistribution()
    for category in categories[:]:
        word_distributions[category] = WordDistribution()
        category_articles = articles.find({'category': category})
        print "====== {}: {} ======".format(category.encode('utf-8'), category_articles.count())
        for article in category_articles:
            sp = SentenceParser(article["title"])
            sp.parse()
            nouns = sp.extract_nouns()
            word_distributions[category].update_dist(nouns)  # カテゴリーの文書全体の単語頻度更新
            total_words_dist.update_dist(nouns)  # 文書全体の単語頻度更新
        word_distributions[category].calc_total_words_dist()

    dump_object(word_distributions, 'mery_category_word_dist.pkl')
    dump_object(word_distributions, 'mery_total_word_dist.pkl')

    # 上位0.1%以上の出現頻度の単語を取り除く
    total_words_dist.calc_total_words_dist()
    top_n_percent_words = total_words_dist.extract_top_n_percent_words(n=0.1)
    print "=== removed words ==="
    for word in top_n_percent_words:
        print word.encode('utf-8')
    # 結果を表示
    for category in categories[:]:
        word_distributions[category].remove_words(top_n_percent_words)  # 出現頻度が多い単語を削除
        print "====  {}  =====".format(category.encode('utf-8'))
        for word, count in sorted(word_distributions[category].total_words_dist.items(), key=lambda x: x[1], reverse=True)[:20]:
            print word.encode('utf-8'), count


if __name__ == "__main__":
    calc_words_dist()