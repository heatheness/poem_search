# -*- coding: utf-8 -*-

"""
Module contains basic functions for handling text
-- clear_request
-- clear_poem
-- get_normal

"""

import pymorphy2
import re

__author__ = 'nyash myash'


delete = re.compile(u'[^а-яА-Я\-ёЁ0-9]+?', re.UNICODE)
clr = re.compile(r'\s+', re.UNICODE)


def rpl(s):
    """
    this func is used in index module for replacing 'ё' with 'е' in words after normalization

    :param s: unicode string
    :type s: str
    :return: unicode string in which letter 'ё' replaced with 'е'
    :rtype: str
    """
    s = s.split()
    s = [i.replace(u'ё', u'е') if u'ё' in i else i for i in s]
    s = u' '.join(s)
    return s


def clear_request(s):
    """
    ATTENTION:
    -- '-' is saved in words like 'что-либо' etc
    -- 'ё' is replaced with 'e'

    :param s: unicode string
    :type s: str
    :return: lowercased unicode string without punctuation and other non-letter symbols
    :rtype: str
    """

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

    ATTENTION:
    -- '-' is saved in words like 'что-либо' etc)
    -- 'ё' is not replaced with 'e'

    :param s: unicode string
    :type s: str
    :return: lowercased unicode string without punctuation and other non-letter symbols
    :rtype: str
    """

    s = s.lower()
    s = delete.sub(' ', s)
    s = clr.sub(u' ', s).strip()
    s = s.split()
    s = [i for i in s if i != u'-']
    s = u' '.join(s)
    return s


def get_normal(word):
    """
    :param word: unicode string
    :type word: str
    :return: list of tuples containing normal form and part of speech
    f.i. [('стать', 'глагол'), ('сталь', 'существительное')]
    :rtype: list
    """

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
    for item in get_normal(u'стали'):
        print item[0], item[1]
    print clear_request(u'Кто-то где-то    и может - это или что-то  Ёж и ёлочка  куда-то')