# -*- coding: utf-8 -*-

"""
Module contains basic functions for handling text
-- clear_request
-- clear
-- get_normal

"""

import pymorphy2
import re

__author__ = 'nyash myash'


delete = re.compile(u'[^а-яА-Я\-ёЁ0-9]+?', re.UNICODE)
clr = re.compile(r'\s+', re.UNICODE)


def yo_replace(s):
    """
    this func is used in index module for replacing 'ё' with 'е' in words after normalization

    :param s: unicode string
    :type s: str
    :return: unicode string in which letter 'ё' replaced with 'е'
    :rtype: str
    """
    s = s.replace(u'ё', u'е')
    return s


def clear(s):
    """
    ATTENTION:
    -- '-' is saved in words like 'что-либо' etc
    -- 'ё' is not replaced with 'e'

    :param s: unicode string
    :type s: str
    :return: lowercased unicode string without punctuation and other non-letter symbols
    :rtype: list
    """

    s = s.lower()
    s = delete.sub(' ', s)
    s = clr.sub(u' ', s).strip()
    s = s.replace(u' - ', u' ')
    s = s.split()

    for i in xrange(len(s)):
        if s[i].startswith(u'-'):
            for j in xrange(len(s[i])):
                if s[i][j] == u'-':
                    continue
                s[i] = s[i][j:]
                break

    for i in xrange(len(s)):
        if s[i].endswith(u'-'):
            for j in reversed(xrange(len(s[i]))):
                if s[i][j] == u'-':
                    continue
                s[i] = s[i][:j+1]
                break
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
        p = (yo_replace(item.normal_form), pos)
        if p not in normal:
            normal.append(p)

    return normal


if __name__ == '__main__':
    w = clear(u'Кто-то где-то    и может - --это или-- что-то-  -Ёж- и- ёлочка  куда-то')

    for item in w:
        item = get_normal(item)
        print item[0][0], item[0][1]
