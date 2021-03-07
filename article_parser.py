import re
from bs4 import BeautifulSoup
from general import *

class ArticleParser():

  def __init__(self, article):
      self.article = article

  def parse_body(self, body, widgets):
    ''' return body with the correct widgets and a list of all images '''
    body_images = []
    for widget in widgets:
      widget_type = widget['parts'][0]['type']
      widget_content = widget['parts'][0]['content']
      if body.find(widget_content) != -1:
        if widget_type == 'IMAGE':
          img = {}
          src = widget['parts'][0]['presentationElement']['article']['imageUrls']['w0-original-q85']
          img['src'] = src
          img_fields = widget['parts'][0]['presentationElement']['fields']
          # add image figcaption under the picture
          img_fig = ''
          if 'caption' in img_fields and 'copyright' in img_fields:
            img['caption'] = img_fields['caption']
            img['copyright'] = img_fields['copyright']
            img_fig = ' <figcaption> '+img['caption']+' <span class="image-credit">Credit: '+img['copyright']+'</span></figcaption>'
          body_images.append(img)
          soup = BeautifulSoup(widget_content, features="html.parser")
          for link in soup.findAll('img'):
              link['src'] = img['src']
              link['width'] = '780'
              link['height'] = '1024'
          new_img = str(soup)
          body = body.replace(widget_content, new_img + img_fig)
    return (body, body_images)

  def get_slug(self, url):
    url_splitted = url.split("/")
    return url_splitted[len(url_splitted)-2] + '/' + url_splitted[len(url_splitted)-1]
  
  def get_category(self, url):
    return url.split("/")[3]

  def parse(self):
    article = {}
    #get the opener
    opener = get_opener(self.article['areas'])
    article['opener'] = opener

    context_article = {}
    if 'contextArticle' in self.article:
      context_article = self.article['contextArticle']

    # only import news articles for testing
    if 'contextArticle' in self.article and context_article['contentType'] == 'news' and opener is not None:
      
      article['articleId'] = context_article['articleId']
      article['category'] = self.get_category(context_article['url'])
      article['keywords'] = context_article['tagNames']
      article['firstPublishedDate'] = context_article['firstPublishedDate']
      article['lastModifiedDate'] = context_article['lastModifiedDate']
      article['contentType'] = context_article['contentType']
      article['title'] = context_article['fields']['title']
      if 'intro' in context_article['fields']:
        article['intro'] = context_article['fields']['intro']

      article['slug'] = self.get_slug(context_article['url'])

      #get the body of the article
      body_widgets = get_body_widgets(self.article['areas'])
      article['body'], article['images'] = self.parse_body(context_article['fields']['body'], body_widgets)

      #get seo fields
      article['seo_title'] = context_article['fields']['seo_title']
      if 'seo_description' in context_article['fields']:
        article['seo_description'] = context_article['fields']['seo_description']
      
      return article
    else:
      return {}
      


