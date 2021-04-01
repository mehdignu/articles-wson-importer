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
      widget_type = widget['type']
      widget_content = widget['content']
      if body.find(widget_content) != -1:
        if widget_type == 'ARTICLE':
          inline_link = get_inline_link(widget)
          body = body.replace(widget_content, inline_link)
        if widget_type == 'FACEBOOK':
          facebook_embed = get_facebook_embed(widget)
          body = body.replace(widget_content, facebook_embed)
        if widget_type == 'INSTAGRAM':
          instagram_embed = get_instagram_embed(widget)
          body = body.replace(widget_content, instagram_embed)
        if widget_type == 'TWITTER':
          twitter_embed = get_twitter_embed(widget)
          body = body.replace(widget_content, twitter_embed)
        if widget_type == 'YOUTUBE':
          youtube_embed = get_youtube_embed(widget)
          body = body.replace(widget_content, youtube_embed)
        if widget_type == 'IMAGE':
          images, new_img, img_fig = get_inline_images(widget, widget_content)
          # save the inline images and group them together
          body_images.append(images)
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
    if 'contextArticle' in self.article and context_article['contentType'] == 'news':
      try:
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
        #for x in body_widgets:
        #  print(x['parts'])
      
        article['body'], article['images'] = self.parse_body(context_article['fields']['body'], body_widgets)
      
        #get seo fields
        article['seo_title'] = context_article['fields']['seo_title']
        if 'seo_description' in context_article['fields']:
          article['seo_description'] = context_article['fields']['seo_description']
        
        return article
      except:
        return {}
    else:
      return {}

      
