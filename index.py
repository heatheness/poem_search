# -*- coding: utf-8 -*-
"""
Module for holding poems and index object.
If you need a poem or data from index - get it from here
Functions:
-- get_poem. returns poem by poem number
-- get_index_data. returns index data by normalized word

"""

__author__ = 'nyash myash'

import codecs
import json
from text_utils import get_normal, clear

def do_list(path = u'oster.txt'):
    """
    takes path to txt file with poems separated with '* * *'.
    returns list of poems

    """

    f = codecs.open(path, encoding=u'utf-8')
    poems = []
    s = u''
    for line in f.readlines():
        if line == u'\n':
            continue
        elif line != u'* * *\n':
            s+= line
        else:
            poems.append(s)
            s = ''
    else:
        if s:
            poems.append(s)
    return poems

def init_index():
    """
    returns index (dict) like {normal_form : [(poem number, position in poem), (poem number, position in poem) ... ]}
    returns index from file if index.txt exists, otherwise creates index and index.txt with create_index func

    """

    global poems

    try:
        with codecs.open('index.txt', 'r', encoding='utf-8') as f:
            r = f.read()
            cur_index = json.loads(r)
            return cur_index
    except IOError:
        create_index()

def create_index():
    """
    returns new index (dict) like {normal_form : [(poem number, position in poem), (poem number, position in poem) ... ]}
    creates index.txt or rewrites index.txt if exists
    """
    global poems
    cur_index = {}

    print "Please wait"
    for i in xrange(len(poems)):
        print 'creating index for poem ...', i
        position = 0
        sen = clear(poems[i]).split()
        for word in sen:
            normal = get_normal(word)
            for item in normal:
                cur_index.setdefault(item[0], []).append((i, position))
            position +=1

    storage_index = json.dumps(cur_index)
    with codecs.open('index.txt', 'w', encoding='utf-8') as f:
        f.write(storage_index)

    return cur_index

def get_poem(i):
    """ returns poem by poem number """

    global poems
    return poems[i]

def get_index_data(word):
    """ returns index data by normalized word """
    global poems_index
    return poems_index[word]


poems = do_list()
poems_index = init_index()

if __name__ == "__main__":
    print len(poems)

    for key in sorted(poems_index.keys()):
        print u'{0:14} ==> {1}'.format(key, poems_index[key])