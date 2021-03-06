#!/usr/bin/env python
from pbwiki import *
from store_wikis import *
from sqlalchemy import text
from sqlalchemy.sql import select

def store_revisions(list_of_dicts):
    for change in list_of_dicts:
        insert = revs_table.insert()
        insert.execute(change)
    return

def fetch_html(url_to_fetch, page_to_fetch, revision_to_fetch):

    pb = PBWiki(url_to_fetch)
    response = pb.api_call('GetPage', page=page_to_fetch, revision=revision_to_fetch)
    if 'html' in response :
        return response['html']
    else:
        return ''

def json_to_dict(response, url_to_fetch):
    newlist = []
    for old in response:
        new = {}
        new['html'] = fetch_html(url_to_fetch, old['title'], old['time'])
        new['user'] = str(old['user'])
        new['page_title'] = old['title']
        new['url'] = old['url']
        new['hash'] = old['hash']
        new['time'] = old['time']
        new['type'] = old['type']
        newlist.append(new)
    return newlist

def change_get(pbojb):
    ccchanges = pbojb.api_call('GetChanges')
    return ccchanges['changes']

def get_checked():
    #query = text("select url,page_title from revisions order by url desc;")
    #Session = sessionmaker(bind=engine)
    #session = Session()
    #table = revs_table.insert()
    #print table.execute(query).fetchall()

    #from sqlalchemy.sql import select

    results = engine.execute(revs_table.select()).fetchall()
    done_wikis = []
    for row in results:
        done_wikis.append(row['url'][:-len(row['page_title'])])

    return done_wikis

    

def get_wikilist():
    # Read the semi-private list of wikis from file
    l = open('./nocheckin/wiki-list.txt', 'r')
    ll = []
    for row in l:
        ll.append(row)    
    return ll

def test_case():
    url = 'http://testapi.pbworks.com'
    pbjelly = PBWiki(url)
    clist = change_get(pbjelly)
    return clist,url

def main():
    url_list = get_wikilist()
    for url in url_list:
        url = url[:-1]
        print url
        pbjelly = PBWiki(url)
        clist = change_get(pbjelly)
        store_list = json_to_dict(clist, url)
        print 'fetched'
        store_revisions(store_list)
        print 'stored!'
        print
    print "all done"

if __name__ == '__main__':
    #main()
    list = get_checked()
