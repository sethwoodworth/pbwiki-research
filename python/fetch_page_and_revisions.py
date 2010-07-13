#!/usr/bin/env python                                                                           
from pbwiki import *
from store_wikis import *
from sqlalchemy import Text
import sqlalchemy as sql



def save_rev(url, page, save_dict):
    dict = {}
    dict['url'] = url
    dict['page_title'] = page

    dict['author'] = str(save_dict['author']['name'])
    dict['author_uid'] = str(save_dict['author']['uid'])
    dict['html'] = str(save_dict['html'])
    dict['time'] = int(save_dict['mtime'])
    dict['hash'] = str(save_dict['oid'])
    dict['revision'] = int(save_dict['revcount'])
    dict['revurl'] = str(save_dict['revurl'])
    dict['char_size'] = str(save_dict['size'])
    dict['wikistyle'] = str(save_dict['wikistyle'])

    i = revs_table.insert()                                                                    
    i.execute(dict)


def pb_api_calls(url, page):
    print url
    wiki_api = PBWiki(url)
    arg = {"page" : page}
    print arg
    data_d = {}
    rev_list = wiki_api.api_call('GetPageRevisions', **arg)['revisions']
    for rev in rev_list:
        print rev
        kwarg = {"revision": rev, "page": page}
        data_d[rev] = wiki_api.api_call('GetPage', **arg)
    for save in data_d:
        save_rev(url, page, save)    

        

def load_revs(url, page):
    print page
    api_return = pb_api_calls(url, page)

def recall_wikis():
    query = "select url,pages_list from edu_wikis where have_pages=0 and works=1;"
    pageless_wikis = engine.execute(sql.text(query)).fetchall()
    return pageless_wikis

def fetch_all(debug = False):
    if debug:
        print "Status:**** Debugmode active****"
        wikis_tuples = recall_wikis()
    else:
        wikis_tuples = recall_wikis()

    for t in wikis_tuples:
        url = t[0]
        pages = eval(t[1])
        #print url
        [load_revs(url, page) for page in pages]

    #for wiki in wikis_list:
    #    print "Status:     retreving and storing url  " + str(wiki)
    #    api_response = pb_api_calls(wiki)
    #    save_wiki(wiki, api_response)

if __name__ == '__main__':
    plist = fetch_all(debug = True)
