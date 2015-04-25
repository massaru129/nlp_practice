# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from base_crawler import BaseCrawler


def mery_crawler():
    root_url = 'http://mery.jp'
    categories = ['fashion', 'cosme', 'hairstyle', 'nail', 'beauty', 'gourmet', 'travel', 'love', 'lifestyle']
    rules = {'article': {'title': ['h1'],
                         'content': ['.articleArea p.article_text', '.articleArea p.article_image_desc', '.articleArea h2.article_headline'],
                         'pv': ['li.view span'],
                         'keywords': ['li.tag a'],
                         'category': ['ul.topBar_in li a span']},
             'links': 'h3.article_list_title a'}
    for category in categories[:1]:
        category_root_url = '/'.join([root_url, category])
        crawler = BaseCrawler(root_url=category_root_url, rules=rules, databse='mery')
        crawler.run(start_page=1, end_page=2)


if __name__ == '__main__':
    mery_crawler()