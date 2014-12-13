# -*- coding: utf-8 -*-

"""
Module contains basic functions for handling text
-- clear_request.  returns string without digits, punctuation and non-cyrillic letters, 'ё' is replaced with 'е'
-- clear_poem. like clear_request, but 'ё' is not replaced with 'е'
-- normalizing words
"""

__author__ = 'nyash myash'


import pymorphy2
import re


delete = re.compile(u'[^а-яА-Я\-ёЁ0-9]+?', re.UNICODE)
clr = re.compile(r'\s+', re.UNICODE)
# replace = re.compile(u'ё', re.UNICODE)


def rpl(s):
    """
    returns string in which letter 'ё' replaced with 'е'
    this func is used in index module for replacing 'ё' in words after normalization

    """

    # return replace.sub(u'e', s)
    s = s.split()
    s = [i.replace(u'ё', u'е') if u'ё' in i else i for i in s]
    s = u' '.join(s)
    return s


def clear_request(s):
    """
    takes a string,
    returns lowercased string without digits, punctuation and non-cyrillic letters
    ATTENTION:
    -- '-' is saved in words like 'что-либо' etc)
    -- 'ё' is replaced with 'e' """

    s = s.lower()
    s = delete.sub(' ', s)
    s = clr.sub(u' ', s).strip()
    s = s.split()
    s = [i for i in s if i != u'-']
    s = [i.replace(u'ё', u'е') if u'ё' in i else i for i in s]
    s = u' '.join(s)
    return s

def clear_poem(s):
    """
    THIS FUNC IS USED IN INDEX CREATION

    takes a string,
    returns lowercased string without digits, punctuation and non-cyrillic letters
    ATTENTION:
    -- '-' is saved in words like 'что-либо' etc)
    -- 'ё' is not replaced with 'e'


    """

    s = s.lower()
    s = delete.sub(' ', s)
    s = clr.sub(u' ', s).strip()
    s = s.split()
    s = [i for i in s if i != u'-']
    s = u' '.join(s)
    return s


def get_normal(word):
    """takes single word, returns list of tuples containing normal form and part of speech
    f.i. [('стать', 'глагол'), ('сталь', 'существительное')]
    if part of speech can not be defined than part of speech is None"""

    pos_match = {
        u'NOUN': u'существительное',
        u'ADJF': u'прилагательное',
        u'ADJS': u'прилагательное',
        u'COMP': u'наречие',
        u'VERB': u'глагол',
        u'INFN': u'глагол',
        u'PRTF': u'причастие',
        u'PRTS': u'причастие',
        u'GRND': u'деепричастие',
        u'NUMR': u'числительное',
        u'ADVB': u'наречие',
        u'NPRO': u'местоимение',
        u'PRED': u'наречие',
        u'PRCL': u'частица',
        u'CONJ': u'союз',
        u'PREP': u'предлог',
        u'INTJ': u'междометие',
    }

    morph = pymorphy2.MorphAnalyzer()
    forms = morph.parse(word)
    normal = []
    for item in forms:
        pos = item.tag.POS
        if pos in pos_match.keys():
            pos = pos_match[pos]
        p = (item.normal_form, pos)
        if p not in normal:
            normal.append(p)
    return normal


if __name__ == '__main__':
    # print get_normal(u'стали')
    c = {}
    for item in get_normal(u'вперёд'):
        print item[0], item[1]
    print clear_request(u'Кто-то где-то    и может - это или что-то  Ёж и ёлочка  куда-то')