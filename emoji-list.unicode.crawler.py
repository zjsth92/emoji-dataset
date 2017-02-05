#!/usr/bin/env python
"""This module is used to crawler emoji unicode from http://www.unicode.org/ """
import urllib
import json
import base64
import os
from bs4 import BeautifulSoup

__EMOJI_V4_URL = "http://www.unicode.org/emoji/charts/emoji-list.html"
__EMOJI_V5_URL = "http://www.unicode.org/emoji/charts-beta/emoji-list.html"
__IMG_FOLDER_NAME = "emoji_imgs"


def decode_base64(data):
    """Decode base64, padding being optional.
    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.
    """
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += b'=' * missing_padding
    return base64.decodestring(data)


def crawler_emojis(version):
    # create folder
    dir_path = __IMG_FOLDER_NAME+'_'+version
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    URL = ''
    if version == 'V4':
        URL = __EMOJI_V4_URL
    elif version == 'V5':
        URL = __EMOJI_V5_URL

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
        # encode img
        img_base64 = _img_list[i]
        img_data = decode_base64(img_base64[21:])
        name_to_save = _code_list[i] + ".png"
        # save img to disk
        print name_to_save
        with open(dir_path + "/" + name_to_save, "wb") as f:
            f.write(img_data)
            f.close()

        # write data in json form
        data = {"unicode": _code_list[i],
                "name": _name_list[i], "img": name_to_save}
        _json_list.append(data)
    
    data_file_name = version+'_data.json'
    with open(data_file_name, 'w') as outfile:
        json.dump(_json_list, outfile)

    print "Done version "+version+"\n"

crawler_emojis('V4')
crawler_emojis('V5')