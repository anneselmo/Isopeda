#! /usr/bin/python3

import pickle
import json

from collections import Counter

import utils
import corpse

def load_cl(classifier): #load the classifier from a saved file
    f=open(classifier, "rb")
    return(pickle.load(f))

def score_cdb(tfile, cats, keywords, cl):
    cdb=utils.open_cdb(tfile)
    score, uscore={}, {}
    for key in utils.get_all_keys(cdb):
        if key.endswith("desc"):
                cati=check_categories(cl, cats, json.loads(str(cdb[bytes(key, 'utf-8')], 'utf-8')))
                keywi=check_keywords(keywords, str(cdb[bytes(key, 'utf-8')], 'utf-8'))
                value=int(cati)+keywi
                score[cdb[bytes(key[:-4]+"url", 'utf-8')]]=value
                print("VAL:", cati, keywi)
    return(score)

def ready_directory(directory):
    for place in utils.recursive_scan("dict.cdb", directory):
        if place.startswith("allwords"):
            allwords=utils.cdb2dict(place)
    corpse.neo_process_dir(directory)

def check_keywords(keywords, descr):
    score=0
    descr=json.loads(descr)
    for word in descr:
        if descr[word] > 1:
            if word in keywords:
                score=score+descr[word]
    return(score)

def check_categories(cl, cats, descr):
    cat=cl.classify(descr)
    print(cat)
    if str(cat, 'utf-8') in cats:
        print(cats[str(cat, 'utf-8')])
        return(cats[str(cat, 'utf-8')])
    return(0)

def isopeda(directory, confdir):
    score={}
    best=[]
    global allwords
    cats=load_json(confdir+"/"+"cats.dict")
    allwords=utils.cdb2dict(confdir+"/"+"allwords.dict.cdb")
    keywords=load_json(confdir+"/"+"keywords.list")
    cl=load_cl("classi.class") 
    ready_directory(directory)
    places=utils.recursive_scan("desc.cdb", directory)
    for place in places:
        score.update(score_cdb(place, cats, keywords, cl))
    print(score)

    leaderboard=Counter(score)
    print(leaderboard.most_common(5))
            
def load_json(tfile):
    with open(tfile, "r") as source:
        return(json.load(source))
