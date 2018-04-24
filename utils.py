#!/usr/bin/py

import os
import cdbx
import json

def recursive_scan(extension, directories):
    filelist=[]
    for directory in directories:
        for (root, dirnames, filenames) in os.walk(directory):
            for filename in filenames:
                if filename.endswith(extension):
                    filelist.append(os.path.join(root, filename))
    return(filelist)

def get_all_keys(cdb):
    keylist=[]
    try:
        keys=cdb.keys(all=True)
    except OSError as err:
        print(err)
        return(keylist)
    for key in keys:
        keylist.append(str(key, 'utf-8'))
    return(keylist)
             
def open_cdb(tfile):
    return(cdbx.CDB(tfile))

def neo_cdb(tfile):
    return(cdbx.CDB.make(tfile))

def ccommit_cdb(cdb):
    cdb.commit().close()

def cdb_add(cdb, key, content):
    if type(key) is bytes:
        pass
    else:
        key=bytes(key, 'utf-8')
    if type(content) is bytes:
        pass
    else:
        content=bytes(content, 'utf-8')
    cdb.add(key, content)

def find_directories(path):
    dlist=[]
    for path in os.listdir(path):
        if os.path.isdir(path) is True:
            dlist.append(path)
    return(dlist)

def dict2cdb(content, name):
    cdb=neo_cdb(name)
    for item in content:
        try: 
            cdb_add(cdb, item, content[item])
        except:
            cdb_add(cdb, item, json.dumps(content[item]))
    ccommit_cdb(cdb)
    return(0)

def cdb2dict(tfile):
    cdb=open_cdb(tfile)
    ndict={} 
    for key in cdb.keys(all=True):
        ndict[key]=cdb[key]
    return(ndict)
