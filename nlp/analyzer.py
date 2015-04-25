# -*- coding; utf-8 -*-
__author__ = 'masaru'

import sys
sys.path.append('..')
from db.mongodb import MongoDB
from tools.parser import SentenceParser
from utils.pickle_tool import dump_object, load_object
from tools.word_distribution import WordDistribution


def main():
    mongo = MongoDB(host='localhost', port=27017, db_name='mery')
    mongo.load_database()
    articles = mongo.load_collection('articles')
    word_distribution = WordDistribution()
    for article in articles.find():
        sp = SentenceParser(article["title"][0])
        sp.parse()
        nouns = sp.extract_nouns()
        word_distribution.update_dist(nouns)
    word_distribution.show_result()
    dump_object(word_distribution, 'mery_word_dist.pkl')


if __name__ == "__main__":
    main()
