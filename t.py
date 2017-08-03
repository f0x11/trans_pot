#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib

import requests
import time
from translate.convert.pot2po import convert_stores
from translate.storage import factory

__author__ = 'f0x11'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'fanyi.youdao.com',
    'Origin': 'http://fanyi.youdao.com',
    'Referer': 'http://fanyi.youdao.com/',
    'X-Requested-With': 'XMLHttpRequest',
}

cookies = {
    'UM_distinctid': '15da6b5edec307-097078436cf011-30657808-232800-15da6b5eded5a8',
    'JSESSIONID': 'aaaQzg3y2x6uE4FvJTM2v',
    'SESSION_FROM_COOKIE': 'fanyiweb',
    'OUTFOX_SEARCH_USER_ID': '454835555@111.200.217.34',
    '_ntes_nnid': 'b80b924987c16093da52103bdbbc7f0e,1501740548355',
    'OUTFOX_SEARCH_USER_ID_NCOO': '555546042.8361456',
    '___rl__test__cookies': '1501741069310',
}


def trans_word(input_word):
    youdao_url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule&sessionFrom='
    salt = '1501741069312'
    client = 'fanyideskweb'
    g = hashlib.md5(client + input_word + salt + "rY0D^0'nM0}g5Mm1z%1G4").hexdigest()
    result = requests.post(youdao_url, data={
        'i': input_word,
        'from': 'en',
        'to': 'zh - CHS',
        'smartresult': 'dict',
        'client': client,
        'salt': salt,
        'sign': g,
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_CLlCKBUTTON',
        'typoResult': 'true',
    }, headers=headers, cookies=cookies)

    if result.status_code != 200:
        print result
        raise Exception
    try:
        output_word = result.json()['translateResult'][0][0]['tgt']
    except:
        print result
        return False, ''

    return True, output_word


def trans_file(input_file, output_file, min_similarity=75, fuzzymatching=True,
               classes=None, classes_str=factory.classes_str, **kwargs):
    input_store = factory.getobject(input_file, classes=classes,
                                    classes_str=classes_str)

    try:
        temp_store = factory.getobject(input_file, classes_str=classes_str)
    except Exception:
        # StringIO and other file like objects will be closed after parsing
        temp_store = None

    for unit in input_store.unit_iter():
        ok, out_word = trans_word(unit.source)
        if ok:
            unit.target = out_word
            time.sleep(0.5)

    output_store = convert_stores(input_store, temp_store, None, None,
                                  min_similarity, fuzzymatching, **kwargs)
    output_store.serialize(output_file)

    return 1


if __name__ == "__main__":
    input_file = 'openshift.pot'
    output_file = 'openshift.po'
    with open(output_file, 'w+') as outfile_p:
        trans_file(input_file, outfile_p)
