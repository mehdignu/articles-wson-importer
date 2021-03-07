
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
                                    return x['widgetFields']['paragraphs']