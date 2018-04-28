#! /usr/bin/python3

#training and set management
import utils

import json
import os
import nltk
import random
import pickle

def open_desc(tfile):
    cdb=utils.open_cdb(tfile)
    dlist=[]
    klist=utils.get_all_keys(cdb)
    cat=cdb["description"]
    for key in klist:
        if key.endswith("desc"):
            dlist.append((json.loads(str(cdb[bytes(key, 'utf-8')], 'utf-8')), cat))
    return(dlist)

def equalize_sets(pile):
    index, i={}, 0
    for item in pile:
        try: 
            index[item[1]]=index[item[1]]+1
        except: 
            index[item[1]]=0
    print(index) 
    random.shuffle(pile)
    for item in pile:
        if index[item[1]] > 0:
            index[item[1]]=index[item[1]]-1
            pile.pop(i)
            i=i+1
    return(pile) 

def gen_sets(path):
    clist=[]
    for tfile in os.listdir(path):
        if tfile.endswith("desc.cdb"):
            clist=clist+open_desc(path[:-1]+tfile)
    random.shuffle(clist)
    return(clist)

def breakup_sets(pile):
    split=round(len(pile))/2
    return([pile[:split], pile[split:]])

def train_set(tset):
    return(nltk.NaiveBayesClassifier.train(tset))

def save_classifier(classifier, destfile):
    f=open(destfile, "wb")
    pickle.dump(classifier, f)
    f.close()

def classi(path):
    sets=breakup_sets(gen_sets(path))
    cl=train_set(sets[0])
    print("accuracy ish:", nltk.classify.accuracy(cl, sets[1]))
    save_classifier(cl, path+"/classi.class")
    return(0)
