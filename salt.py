#! /usr/bin/python3 
# a webcrawler
import requests
from urllib.parse import urlsplit
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup
import cdbx
import datetime
import os 
import magic
import random

class faux_page: #fake pages when errors occur
    content = None

def trueget(llist):
    database=cdbx.CDB.make(datetime.datetime.now().strftime("%s")+".html.cdb")
    global neo_list 
    for link in llist:
        print("NEOLIST:", len(neo_list), "\nGOTLIST:", len(got_list))
        if link is None:
            pass
        elif not link.startswith('https://') and not link.startswith('http://'): #http/s only
            pass
        else:
            bowl=data_enter(link, database)
            if bowl==1:
                pass
            else:
                neo_list = (linksget2(bowl, findbaseurl(link)) + neo_list)
    database.commit().close()
    return(neo_list)

def data_enter(url, database):
    data=pagegets(url)
    if data[1] is 3:
        return(1) #dont keep blanks
    page=data[0]
    scan=magic.Magic(mime=True)
    url.replace("\n", "")
    if url.split(".")[-1:][0] in ["zip", "gzip", "tgz", "iso", "xz", "bz2", "img", "qcow2", "mp3", "aac", "flac", "opus", "mp4", "ogg"]:
        print("FISHFISHFISHFISH")
        del(page)
        return(1)
    if scan.from_buffer(page.content) is "<html></html>": #dont save blank pages
        del(page)
        return(1)
    database.add(bytes("ut-"+url, 'utf-8'), datetime.datetime.now().strftime("%s")) #timestamping
    database.add(bytes("vr-"+url, 'utf-8'), data[1]) #https status
    if scan.from_buffer(page.content).startswith('text'):
        soup=BeautifulSoup(page.content)
        database.add(bytes(url, 'utf-8'), bytes(str(soup.contents), 'utf-8'))
        del(page)
        return(soup)
    else:
        database.add(bytes(url, 'utf-8'), page.content) #store binaries
        del(page)
        return(1)

def findbaseurl(url): #find the url to append if links arent absolute
    return("{0.scheme}://{0.netloc}".format(urlsplit(url)))

def pagegets(url): #download 
    global got_list
    if url in got_list:
        return(return_blank_page())
    else:
        got_list = (got_list+[url])
        try:
            if findbaseurl(url).endswith('.onion'): 
                tor=requests.session()
                tor.proxies= { 'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050' }
                page=tor.get(url, verify=False, headers={"User-Agent": "Salticus scenicus"})
            else:
                try:
                    page = requests.get(url, headers={"User-Agent": "Salticus scenicus"}) 
                    https=1
                except:
                    page = requests.get(url, verify=False, headers={"User-Agent": "Salticus scenicus"}) #ignore https errors
                    https=0
        except requests.exceptions.RequestException:
            page=return_blank_page()
            https=3
        return(page, https)

def return_blank_page():
    page=faux_page
    page.content="<html></html>"
    return(page)

def linksget2(page, rooturl): #derives a list of links from an html page
    llist = []
    for link in page.findAll('a'):
        visible = link.get('href')
        if visible is None:
            pass
        elif visible.startswith('/'):
            llist.append((rooturl) + (visible))
        elif visible.startswith('#'):
            pass
        else:
            llist.append(visible)
    for word in page.text.split():
        if word.startswith("http"):
            llist.append(word)
    print('LLIST:', len(llist))
    return(list(set(llist))) #fixes duplication

def nameclean(name): #fixes filenames 
    return(name.replace("/", "-"))

def countloop(pre_list, rounds, limit, threads, place):
    global got_list, neo_list
    root=os.path.abspath(".")
    got_list = []
    neo_list = pre_list
    i=0
    pool=Pool(threads)
    if type(place) is str:
        path=place
    else:
        path=root+"/"+datetime.datetime.now().strftime("%F.%T")

    print(path, root)
    try:
        os.mkdir(path)
        os.chir(path)
    except:
        os.chdir(path)
    
    os.mkdir("crawl")
    os.chdir("crawl")

    neo_list=trueget(neo_list)
    while i < rounds:
        print("THREADS")
        pool.map(trueget, list_byte(24))
        i=i+1
        if i > 2:
            neo_list=nlistclean(pre_list)
        if len(neo_list) > limit:
            neo_list=random.sample(neo_list, limit)
    return("f")

def list_byte(size):
    count=round(len(neo_list)/size)+1
    return([neo_list[x:x+count] for x in range(0, len(neo_list), count)])

def nlistclean(flist):
    global neo_list
    print("listclean")
    elist, nflist=[], got_list
    for url in flist:
        nflist.append(findbaseurl(url))
    for url in neo_list:
        if findbaseurl(url) not in nflist:
            elist.append(url)
        else:
            print("filtered", url)
    neo_list=elist
    return(neo_list)
