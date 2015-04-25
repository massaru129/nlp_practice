# nlp_practice
nlpの基本的な分析ツールとデータ収集や処理に必要なクローラーや形態素解析器など

* `crawler`
  * base_crawlerを元にクローリング対象ごとのクローラーを`crawler/crawlers`以下に作る
* `db`
  * mongoDB周りの処理を記述
* `nlp`
  * `nlp/tools`以下に形態素解析器や単語頻度分析のスクリプトを配置
  * `nlp/dict`以下にigo-python用の辞書を配置する必要がある。igo-pythonの辞書作成方法は[こちら](http://qiita.com/ru_pe129/items/0d39e94862cb558015f0)
  * `nlp/utils`以下に細々した便利スクリプトを配置
* `requirements.txt`
  * 必要なライブラリ
