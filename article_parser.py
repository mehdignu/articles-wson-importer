import re
from bs4 import BeautifulSoup

class ArticleParser():

  def __init__(self, article):
      self.article = article


  def get_opener(self, areas):
    ''' get the opener of the article '''
    opener = {}
    for ar in areas:
      if 'areaName' in ar:
          if ar['areaName'] == 'config_main':
              for ars in ar['groups']:
                  if ars['groupName'] == 'config_article_with_sidebar':
                      arb = ars['groups']
                      for b in arb:
                          if b['groupName'] == 'header':
                              c = b['widgets']
                              for x in c:
                                  if x['widgetView'] == 'article_opener' and x['elementsTotalCount'] > 0:
                                      opener['openerType'] = x['widgetName']
                                      opener['url'] = x['elements'][0]['article']['imageUrls']['w0-original-q85']
                                      opener['openerTitle'] = x['elements'][0]['article']['fields']['title']
                                      opener['openerCaption'] = x['elements'][0]['article']['fields']['caption']
                                      opener['openerCopyright'] = x['elements'][0]['article']['fields']['copyright'] 
                                      return opener

  def get_body_widgets(self, areas):
    ''' get the body widgets '''
    for ar in areas:
      if 'areaName' in ar:
          if ar['areaName'] == 'config_main':
              for ars in ar['groups']:
                  if ars['groupName'] == 'config_article_with_sidebar':
                      arb = ars['groups']
                      for b in arb:
                          if b['groupName'] == 'body':
                              c = b['widgets']
                              for x in c:
                                  if 'paragraphs' in x['widgetFields']:
                                      return x['widgetFields']['paragraphs']

  def parse_body(self, body, widgets):
    ''' return body with the correct widgets and a list of all images '''
    for widget in widgets:
      widget_type = widget['parts'][0]['type']
      widget_content = widget['parts'][0]['content']
      if body.find(widget_content) != -1:
        if widget_type == 'IMAGE':
          img_src = widget['parts'][0]['presentationElement']['article']['imageUrls']['w0-original-q85']
          soup = BeautifulSoup(widget_content)
          for link in soup.findAll('img'):
              link['src'] = img_src
          new_img = str(soup)
          body = body.replace(widget_content, new_img)
    return body

  def parse(self):
    # only import news articles for testing
    if 'contextArticle' in self.article and self.article['contextArticle']['contentType'] == 'news':
      article = {}
      article['articleId'] = self.article['contextArticle']['articleId']
      article['keywords'] = self.article['contextArticle']['tagNames']
      article['firstPublishedDate'] = self.article['contextArticle']['firstPublishedDate']
      article['lastModifiedDate'] = self.article['contextArticle']['lastModifiedDate']
      article['contentType'] = self.article['contextArticle']['contentType']
      article['title'] = self.article['contextArticle']['fields']['title']
      article['intro'] = self.article['contextArticle']['fields']['intro']

      #get the body of the article
      body_widgets = self.get_body_widgets(self.article['areas'])
      article['body'] = self.parse_body(self.article['contextArticle']['fields']['body'], body_widgets)

      #get seo fields
      article['seo_title'] = self.article['contextArticle']['fields']['seo_title']
      article['seo_description'] = self.article['contextArticle']['fields']['seo_description']
      #get the opener
      opener = self.get_opener(self.article['areas'])
      article['opener'] = opener
      return article
    else:
      return {}
      


