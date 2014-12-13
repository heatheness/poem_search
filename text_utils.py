# -*- coding: utf-8 -*-

"""
Module contains basic functions for handling text
-- cleaning string
-- normalizing words
"""

__author__ = 'nyash myash'


import pymorphy2
import re

delete = re.compile(u'[^а-яА-Я\-ёЁ]+?', re.UNICODE)
clr = re.compile(r'\s+', re.UNICODE)

def clear(s):
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
    s = [i.replace(u'ё', u'e') if u'ё' in i else i for i in s]
    s = u' '.join(s)
    return s


def get_normal(word):
    """takes single word, returns list of tuples containing normal form and part of speech
    f.i. [('стать', 'глагол'), ('сталь', 'существительное')]"""

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
    p_speech = []
    for item in forms:
        p = item.normal_form
        if p not in normal:
            normal.append(p)
            if item.tag.POS:
                p_speech.append(pos_match[item.tag.POS])
    return zip(normal, p_speech)

if __name__ == '__main__':
    print get_normal(u'стали')
    print clear(u'Кто-то где-то    и может - это или что-то  Ёж и ёлочка  куда-то')