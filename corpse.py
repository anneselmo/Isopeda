#! /usr/bin/python3

#generate descriptions of text articles
import cdbx
import os
import json

from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize 
from nltk.stem import PorterStemmer as ps
from nltk.tokenize import RegexpTokenizer

import aggtext
import utils

def gen_word_list(page): #find significant words from a text
    tkzr = RegexpTokenizer(r'\w+')
    tokens = tkzr.tokenize(page)
    wlist=[]
    for word in tokens:
        lword=word.lower()
        if lword not in stopwords.words('english'):
            if len(word) > 2:
                wlist.append(ps().stem(lword))
    return(Counter(wlist))
  
def prescan(text, title): 
    global allwords
    try:
        print("ALLWORDS:", len(allwords))
    except:
        allwords={}
    for word in gen_word_list(title):
        if word in allwords:
            allwords[word]=allwords[word]+2
        else:
            allwords[word]=2
    for word in gen_word_list(text):
        if word in allwords:
            allwords[word]=allwords[word]+1
        else:
            allwords[word]=1

def neo_describe(text, title): #generate a pages description using allwords
    wlist=text.lower().split()
    tlist=title.lower().split()
    topics={}
    for word in allwords:
        topics[str(word, 'utf-8')]=allwords[word]
    for word in topics:
        if word in wlist:
            topics[word] = topics[word]+1
        if word in tlist:
            topics[word] = topics[word]+2
    return(topics)

def preprocess_dir(directory): #generate list of significant words
    global allwords
    allwords ={}
    for path in utils.find_directories(directory):
        book=aggtext.agg_text(utils.recursive_scan(".html.cdb", [path]))
        for page in book:
            prescan(page, book[page])
        oallwords=[]
        for word in allwords:
            if word.isalpha() is False:
                oallwords.append(word)
            if allwords[word] < 5:
                oallwords.append(word)
    for word in oallwords:
        try:
            allwords.pop(word)
        except:
            print("err")
    print("ALLWORDS", len(allwords)) 
    utils.dict2cdb(allwords, "allwords.dict.cdb")

def neo_process_dir(directory):
    global allwords
    try: #open allwords if its not already here
        type(allwords) 
    except:
        allwords=utils.cdb2dict(directory+"/allwords.dict.cdb")

    for path in utils.find_directories(directory):
        cdb=utils.neo_cdb(path+".desc.cdb")
        desc=os.path.basename(path)
        book=aggtext.agg_text(utils.recursive_scan(".html.cdb", [path]))
        for word in allwords:
            allwords[word]=0
        for page in book:
            if page.startswith("url") is False:
                utils.cdb_add(cdb, page, book[page])
                utils.cdb_add(cdb, page+"desc", json.dumps(neo_describe(book[page], page)))
                utils.cdb_add(cdb, page+"url", book["url-"+page])
        utils.cdb_add(cdb, "description", desc)
        utils.ccommit_cdb(cdb)
    return("fin")
