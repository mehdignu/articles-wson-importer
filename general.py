from bs4 import BeautifulSoup
import requests

def get_opener(areas):
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
                                if x['widgetView'] == 'article_opener' and x['elementsTotalCount'] > 0 and 'imageUrls' in x['elements'][0]['article']:
                                    opener['openerType'] = x['widgetName']
                                    opener['url'] = x['elements'][0]['article']['imageUrls']['w0-original-q85']
                                    opener_fields = x['elements'][0]['article']['fields']
                                    if 'title' in opener_fields and 'caption' in opener_fields and 'copyright' in opener_fields:
                                      opener['openerTitle'] = ['title']
                                      opener['openerCaption'] = x['elements'][0]['article']['fields']['caption']
                                      opener['openerCopyright'] = x['elements'][0]['article']['fields']['copyright'] 
                                    return opener

def get_body_widgets(areas):
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
                                    widgets = []
                                    widgets_arr = x['widgetFields']['paragraphs']
                                    for f in widgets_arr:
                                        for i, v in enumerate(f['parts']):
                                            if v['content'] and v['type']:
                                                widgets.append(v)
                                    return widgets
  
                                    
### parse inline elements ###

def get_youtube_embed(youtube_widget):
    ''' get the youtube html embed from video id '''
    youtube_fields = youtube_widget['presentationElement']['article']['fields']

    videoID = youtube_fields['videoid']
    youtube_html = '<iframe width="420" height="315" src="http://www.youtube.com/embed/'+ videoID +'" frameborder="0" allowfullscreen></iframe>'
    youtube_title = ''
    if 'teaser_title' in youtube_fields:
        youtube_title = '<figcaption>' + youtube_fields['teaser_title'] + '</figcaption>'
    return youtube_html + youtube_title
    

def get_inline_images(widget, widget_content):
    img = {}
    body_images = []
    src = widget['presentationElement']['article']['imageUrls']['w0-original-q85']
    img['src'] = src
    img_fields = widget['presentationElement']['fields']
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
    return (body_images, new_img, img_fig) 

def get_twitter_embed(twitter_widget):
    ''' get the twitter embed html from the twitter id '''
    twitter_fields = twitter_widget['presentationElement']['article']['fields']
    twitter_embedid = twitter_fields['embed_id']
    embReqUrl = 'https://publish.twitter.com/oembed?url=https%3A%2F%2Ftwitter.com%2FInterior%2Fstatus%2F'+twitter_embedid
    x = requests.get(embReqUrl)
    if x.status_code == 200:
        return x.json()['html']
    else:
        return ''
