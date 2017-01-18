#!/usr/bin/env python
"""This module is used to crawler emoji unicode from http://www.unicode.org/ """
import urllib
import json
from bs4 import BeautifulSoup

__EMOJI_V4_URL = "http://www.unicode.org/emoji/charts/emoji-list.html"
__EMOJI_V5_URL = "http://www.unicode.org/emoji/charts-beta/emoji-list.html"

__PAGE = urllib.urlopen(__EMOJI_V4_URL)
__HTML = __PAGE.read()
__PAGE.close()

__SOUP = BeautifulSoup(__HTML, 'html.parser')

_code_list = []
_img_list = []
_name_list = []
for td in __SOUP.find_all("td"):
    _class_name = td.get("class")[0]
    if _class_name == "code":
        _code_list.append(td.a.get_text())
    elif _class_name == "andr":
        _img_list.append(td.a.img.get("src"))
    elif _class_name == "name":
        _name_list.append(td.get_text())

_json_list = []
for i in range(len(_code_list)):
    data = {"unicode":_code_list[i], "name": _name_list[i], "img": _img_list[i]}
    _json_list.append(data)

with open('data.txt', 'w') as outfile:
    json.dump(_json_list, outfile)

print "Done\n"
