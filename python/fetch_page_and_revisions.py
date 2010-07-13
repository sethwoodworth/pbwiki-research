#!/usr/bin/env python                                                                           
from pbwiki import *
from store_wikis import *
from sqlalchemy import Text
import sqlalchemy as sql



def save_wiki(url, json_dict):
    dict = {}
    dict['url'] = url
    try:
        dict['files_count'] = int(json_dict['GetFiles']['_total_count'])
        dict['files_list'] = str([x['name'] for x in json_dict['GetFiles']['files']])

        dict['page_char_size'] = str(json_dict['page']['size'])
        dict['page_html'] = str(json_dict['page']['html'])
        dict['page_name'] = str(json_dict['page']['name'])
        dict['page_revision'] = int(json_dict['page']['revcount'])

        dict['pages_count'] = int(json_dict['GetPages']['_total_count'])
        dict['pages_list'] = str([x['name'] for x in json_dict['GetPages']['pages']])

        dict['time_pageedit'] = int(json_dict['GetTimes']['pagetime'])
        dict['time_file'] = int(json_dict['GetTimes']['filetime'])
        dict['time_tag'] = int(json_dict['GetTimes']['tagtime'])
        dict['time_permission'] = int(json_dict['GetTimes']['permtime'])
        dict['time_comment'] = int(json_dict['GetTimes']['commenttime'])
        dict['times_checked_at'] = int(json_dict['GetTimes']['_valid_as_of'])

        dict['works'] = 1
    except:
        dict['works'] = 0
    

    i = wikis_table.insert()                                                                    
    i.execute(dict)


def pb_api_calls(url):
    wiki_ops = ['GetFiles', 'GetPages', 'GetTimes']
    wiki_api = PBWiki(url)
    json = {}
    for op in wiki_ops:
        json[op] = wiki_api.api_call(op)
    kwarg = {"page" : 'FrontPage'}
    try:
        json['page'] = wiki_api.api_call('GetPage', **kwarg)
    except:
        print "FrontPage doesn't exist for this wiki"
        json['page'] = {'page': {'size': 0, 'html': '', 'page': ''}}
    return json

def filter_wikilist(wiki_list):
    query = "select url from edu_wikis;"
    done = engine.execute(sql.text(query)).fetchall()
    [wiki_list.remove(str(x)[3:-3]) for x in done]
    return wiki_list

def load_wikilist():
    # return wikis from file as a list
    f = open('../nocheckin/wiki-list.txt', 'r')
    wlist = []
    for row in f:
        wlist.append(row[:-1])
    return wlist

def recall_wikis()
    query = "select url,pages from edu_wikis where have_pages = 0 and works = 1';"
    pageless_wikis = engine.execute(sql.text(query)).fetchall()
    return pageles_wikis

def fetch_all(debug = False):
    if debug:
        print "Status:**** Debugmode active****"
        wikis_list = recall_wikis()
    else:
        wikis_list = recall_wikis()
    return wikis_list

    #for wiki in wikis_list:
    #    print "Status:     retreving and storing url  " + str(wiki)
    #    api_response = pb_api_calls(wiki)
    #    save_wiki(wiki, api_response)

if __name__ == '__main__':
    plist = fetch_all(debug = True)
