#! /usr/bin/python3
import json
import argparse
import os
import datetime

import corpse
import salt
import isopeda
import sets

def save_json(ilist, filename):
    with open(filename, "w") as f:
        json.dump(ilist, f)
    return(0)

def str2dict(string):
    out={}
    pairs=[pair.split(":") for pair in string.split(",")]
    for pair in pairs:
        out[pair[0]]=pair[1]
    return(out)

def parse():
    parser = argparse.ArgumentParser(description="news scanner gizmo")
    parser.add_argument("-k", dest = "keywords", default=0, help="keywords", type=str, nargs='+')
    parser.add_argument("-q", dest = "cats", default=0, help="categories in the format: category:value,category:value[...]", type=str)
    parser.add_argument("-c", dest = "crawl", const=1, default=0, help="signals to do a crawl", action='store_const')
    parser.add_argument("-f", dest = "full", const=1, default=0, help="signals to do a full run (crawl + scan)", action='store_const')
    parser.add_argument("-s", dest = "seeds", default=[], help="list of seed urls", type=str, nargs='+')
    parser.add_argument("-l", dest = "limit", default=1296, help="vaugely followed limit for total list of urls during crawl, default 1296", type=int) 
    parser.add_argument("-t", dest = "threads", default=2, help="number of threads to run crawler with, default 2", type=int) 
    parser.add_argument("-d", dest = "dir", default=0, help="where to run a crawl, default date+time", type=int) 
    parser.add_argument("-x", dest = "confdir", default=".", help="directory where config files are (allwords.dict.cdb etc)", type=str) 
    parser.add_argument("-r", dest = "rounds", default=2, help="number of rounds to run crawler with, default 2", type=int) 
    parser.add_argument("-C", dest = "classify", default=0, help="generate the classifier (argument should be ", type=str) 
    args = parser.parse_args()
    
    if args.full is 1:
        args.crawl=1
        args.dir=os.path.abspath(".")+"/"+datetime.datetime.now().strftime("%F.%T")
    if args.keywords is not 0:
        save_json(args.keywords, "keywords.list")
    if args.cats is not 0:
        print(args.cats)
        save_json(str2dict(args.cats), "cats.dict")
    if args.crawl is 1:
        salt.countloop(args.seeds, args.rounds, args.limit, args.threads, args.dir)
    if args.classify is not 0:
        corpse.preprocess_dir(args.classify)
        corpse.neoprocess_dir(args.classify)
        classi.classi(args.classify)
    if args.full is 1:
        print(args.dir, os.path.abspath(args.confdir))
        isopeda.isopeda(args.dir, os.path.abspath(args.confdir))
    else:
        print("specifying the confdir is a good policy, you can use -h to get help")


parse()
