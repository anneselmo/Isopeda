#! /usr/bin/python3
import json

def create_kw_list():
    list=input("Type a space seperated list of keywords to search for:\t").split(" ")
    with open("keywords.list", "w") as f:
        json.dump(list, f)

