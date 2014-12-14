# -*- coding: utf-8 -*-
"""
Module for holding poems and index object.
If you need a poem or data from index - get it from here
Functions:
-- get_poem
-- get_index_data

"""

import codecs
import json
from text_utils import get_normal, clear

__author__ = 'nyash myash'


def poems_to_list(path=u'oster.txt'):
    """
    :param path: path to txt file with poems separated  with '* * *'
    :type path: str
    :returns list of poems
    :rtype: list
    """
    f = codecs.open(path, encoding=u'utf-8')
    poems = []
    s = u''
    for line in f.readlines():
        if line == u'\n':
            continue
        elif line != u'* * *\n':
            s += line
        else:
            poems.append(s)
            s = u''
    else:
        if s:
            poems.append(s)
    return poems


def init_index():
    """
    :return index like {normal_form : [(poem number, position in poem), (poem number, position in poem) ... ]}
    :rtype: dict
    """

    try:
        with codecs.open('index.txt', 'r', encoding='utf-8') as f:
            r = f.read()
            cur_index = json.loads(r)
            return cur_index
    except IOError:
        return create_index()


def create_index():
    """
    returns index and creates index.txt or rewrites index.txt if exists

    :return index like {normal_form : [(poem number, position in poem), (poem number, position in poem) ... ]}
    :rtype: dict
    """

    global poems
    cur_index = {}

    print "Please wait"
    for i in xrange(len(poems)):
        print 'creating index for poem ...', i
        position = 0
        sen = clear(poems[i])
        for word in sen:
            normal = get_normal(word)
            forms = {i[0] for i in normal}
            for item in forms:
                location = (i, position)
                if u'-' in item:
                    parts = {i for i in item.split(u'-')}
                    for p in parts:
                        cur_index.setdefault(p, []).append(location)
                cur_index.setdefault(item, []).append(location)
            position += 1

    storage_index = json.dumps(cur_index)
    with codecs.open('index.txt', 'w', encoding='utf-8') as f:
        f.write(storage_index)

    return cur_index


def get_poem(i):
    """
    :param i: poem number
    :type i: int
    :return poem
    :rtype: str
    """

    global poems
    return poems[i]


def get_index_data(word):
    """
    :param word: normalized word
    :type word: str
    :return index data
    :rtype: list
    """
    global poems_index
    return poems_index[word]

poems = poems_to_list()
poems_index = init_index()

if __name__ == "__main__":
    print len(poems)

    for key in sorted(poems_index.keys()):
        print u'{0:14} ==> {1}'.format(key, poems_index[key])