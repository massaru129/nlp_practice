# -*- coding: utf-8 -*-

__author__ = "masaru"

import time
import requests
from datetime import datetime
from collections import defaultdict
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class BaseCrawler():
    """
    MongoDBにガシガシ突っ込んでいくクローラー
    """
    def __init__(self, root_url, rules, databse, collection='articles'):
        self.root_url = root_url
        self.rules = rules
        self.client = MongoClient('localhost', 27017)
        self.database = self.client[databse]
        self.collection = self.database[collection]

    def get_article_links(self, url):
        """
        カテゴリトップから記事を取得
        :param url:
        :return:
        """
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.content)
            links = [elem.get('href') for elem in soup.select(self.rules['links'])]
            return links
        except:
            return None

    def parse(self, html):
        """
        各記事からコンテンツを取得する
        :param html:
        :return:
        """
        soup = BeautifulSoup(html)
        article = defaultdict(list)
        for item, item_rules in self.rules['article'].items():
            for rule in item_rules:
                try:
                    article[item].extend([elem.text.strip() for elem in soup.select(rule)])
                except IndexError:
                    continue
        return article

    def run(self, start_page=1, end_page=10,):
        """
        ページングがあるページでクローリングを実行
        :param start_page:
        :param end_page:
        :return:
        """
        for page in range(start_page, end_page+1):
            page = str(page)
            url = self.root_url + '?page={}'.format(page)
            print url
            links = self.get_article_links(url)
            for link in links[:]:
                time.sleep(2)  # 間隔をあけてクロール
                html = requests.get(link).content
                article = self.parse(html)
                article['url'] = link
                self.save(article)
            break

    def save(self, article):
        """
        mongoDBに記事を保存
        :param article:
        :return:
        """
        article['created_at'] = datetime.now()
        try:
            self.collection.insert_one(article)
        except DuplicateKeyError:
            pass