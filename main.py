import requests
import xmltodict
import gzip
import json
from article_parser import ArticleParser


url = 'https://www.goldenekamera.de/sitemaps/archive.xml'

res = requests.get(url)
raw = xmltodict.parse(res.text)

# initialize the articles json
with open('data.json', mode='w', encoding='utf-8') as f:
    json.dump([], f)
feeds = []
c = 0
for r in raw["sitemapindex"]["sitemap"]:
    if c == 0:
        c += 1
        continue
    else:
        if c == 2:
            break
        c += 1
    #try:
    resSingle = requests.get(r["loc"], stream=True)
    if resSingle.status_code == 200:
        if resSingle.headers['Content-Type'] == 'application/x-gzip':
            resSingle.raw.decode_content = True
            resSingle = gzip.GzipFile(fileobj=resSingle.raw)
        else:
            resSingle = resSingle.text
        rawSingle = xmltodict.parse(resSingle)
        article_urls = [[rSingle["loc"]]
                        for rSingle in rawSingle["urlset"]["url"]]
        for u in article_urls:
          req = requests.get(
              u[0] + '?wson', verify=False, auth=('wson', 'Abendblatt!'))
          if req.status_code == 200:
            articles_dict = json.loads(req.text)

            with open('data.json', mode='w', encoding='utf-8') as feedsjson:
              art_parser = ArticleParser(articles_dict)
              article = art_parser.parse()
              if len(article) > 0:
                feeds.append(article)
              json.dump(feeds, feedsjson)

   # except:
    #    print('error while importing the articles')
