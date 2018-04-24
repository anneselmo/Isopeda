#! /usr/bin/python3

#aggregate text from webcrawler
import cdbx
import os
import re 
import magic
from bs4 import BeautifulSoup

import utils

def clean_html(html): #stolen from nltk
    clean=""
    # First we remove inline JavaScript/CSS:
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
    # Then we remove html comments. This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
    # Next we can remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
    # Finally, we deal with whitespace
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    for line in cleaned.splitlines(): #it seems like short lines are often trash
        if len(line.split()) >=4:
            clean=clean+line
    return(clean.strip())

def find_title(html):
    soup=BeautifulSoup(html)
    if soup.title is None:
        return("")
    else:
        return(BeautifulSoup(html).title.text)

def agg_text(places):
    neo_dict={}
    for ffile in places:
        print(ffile)
        try:
            cdb=utils.open_cdb(ffile)
            for key in utils.get_all_keys(cdb):
                if key.startswith("http"):
                    scan=magic.Magic(mime=True).from_buffer(cdb[bytes(key, 'utf-8')])
                    print(scan)
                    if scan.startswith('text') is True:
                        print(key)
                        page=clean_html(str(cdb[bytes(key, 'utf-8')], 'utf-8'))
                        if len(page) > 18:
                            title=find_title(str(cdb[bytes(key, 'utf-8')], 'utf-8'))
                            neo_dict[title] = page
                            neo_dict["url-"+title]=key
            cdb.close()
        except:
            pass
    return(neo_dict)
