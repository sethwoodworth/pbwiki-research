#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table
from sqlalchemy import Integer, Text
from sqlalchemy import ForeignKey

engine = create_engine('sqlite:///pbworks.sql')
metadata = MetaData(bind=engine)

wikis_table = Table('edu_wikis', metadata,
    Column('id', Integer, primary_key=True),
    Column('url', Text),

    Column('files_count', Integer),
    Column('files_list', Text),

    Column('page_char_size', Integer),
    Column('page_html', Text),
    Column('page_name', Text),
    Column('page_revision', Integer),
    Column('page_url', Text),

    Column('pages_count', Integer),
    Column('pages_list', Text),

    Column('time_pageedit', Integer),
    Column('time_file', Integer),
    Column('time_tag', Integer),
    Column('time_permission', Integer),
    Column('time_comment', Integer),
    Column('times_checked_at', Integer),

    Column('works', Integer),
    Column('have_pages', Integer, default="0")
    )

pages_table = Table('pages', metadata,
    Column('id', Integer, primary_key=True),
    Column('url', Text, ForeignKey('edu_wikis.url')),
    Column('page', Text),
    Column('have_revs', Integer)
    )

revs_table = Table('revisions', metadata,
    Column('id', Integer, primary_key=True),
    Column('url', Text, ForeignKey('edu_wikis.url')),        # url of wiki
    Column('page_title', Text, ForeignKey('pages.page')), # page
    Column('author', Text),       # whodunnit (username) TODO: Foreign key this to user table
    Column('author_uid', Text),       # whodunnit (username) TODO: Foreign key this to user table
    Column('html', Text),
    Column('time', Integer),    # time of revision
    Column('hash', Text),       # pbworks generated hash (oid) of rev
    Column('revision', Integer),    # time of revision
    Column('revurl', Text),       # pbworks generated hash (oid) of rev
    Column('char_size', Integer),    # of characters according to pb
    Column('wikistyle', Text),       # pbworks generated hash (oid) of rev
    )

metadata.create_all()

if __name__ == '__main__':
    wd = glue()
