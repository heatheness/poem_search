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

delete = re.compile(u'[^а-яА-Я\-ёЁ0-9a-zA-Z]+?', re.UNICODE)
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
    digit_base = {
        u'0': u'о',
        u'3': u'з',
        u'6': u'б',
        u'8': u'в',
        u'1': u''
    }

    latin_base = {
        u'h': u'н',
        u'o': u'о',
        u'e': u'е',
        u'p': u'р',
        u'x': u'х',
        u't': u'т',
        u'y': u'у',
        u'a': u'а',
        u'd': u'д',
        u'k': u'к',
        u'm': u'м',
        u'c': u'с',
        u'b': u'в',
        u'f': u'ф',
    }

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
                s[i] = s[i][:j + 1]
                break

    for i in xrange(len(s)):
        if re.findall(u'\d+[а-яА-Я\-ёЁ]+|[а-яА-Я\-ёЁ]+\d', s[i]):
            for j in s[i]:
                if j in digit_base.keys():
                    s[i] = s[i].replace(j, digit_base[j])

    for i in xrange(len(s)):
        if re.findall(u'[a-zA-Z]+', s[i]):
            for j in s[i]:
                if j in latin_base.keys():
                    s[i] = s[i].replace(j, latin_base[j])
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


def translit(text):
    """
    :param text: unicode string in latin
    :type text: str
    :return: unicode string in cyrillic
    :rtype: str
    """
    base = {
        u'a': u'а',
        u'b': u'б',
        u'v': u'в',
        u'g': u'г',
        u'd': u'д',
        u'e': u'е',
        u'yo': u'е',
        u'zh': u'ж',
        u'z': u'з',
        u'i': u'и',
        u'iy': u'й',
        u'k': u'к',
        u'l': u'л',
        u'm': u'м',
        u'n': u'н',
        u'o': u'о',
        u'p': u'п',
        u'r': u'р',
        u's': u'с',
        u't': u'т',
        u'u': u'у',
        u'f': u'ф',
        u'h': u'х',
        u'ts': u'ц',
        u'ch': u'ч',
        u'sh': u'ш',
        u'sch': u'щ',
        u'"': u'ъ',
        u'y': u'ы',
        u'\'': u'ь',
        u'yu': u'ю',
        u'ya': u'я'
    }

    translitstring = []
    keys = base.keys()
    l = len(text)
    i = 0
    while i < l:
        if i + 3 <= l and text[i:i + 3] in keys:
            k = i + 3
        elif i + 2 <= l and text[i:i + 2] in keys:
            k = i + 2
        else:
            k = i + 1
        translitstring.append(base[text[i:k]])
        i += k - i
    return ''.join(translitstring)


if __name__ == '__main__':
    w = clear(u'Кто-то где-то    и может - --это или-- что-то-  -Ёж- и- ёлочка  куда-то')
    for item in w:
        print item
    print

    w = clear(u'0дывлоа 185 0ыоало0ыдлао ыатдло0 8ывла8 длолдао33апт 0статься 03')
    for item in w:
        print item
    print

    w = clear(u'60дATь')
    print w[0]
    print

    p = get_normal(clear(u'60дAtь')[0])
    for item in p:
        print item[0], item[1]

    print translit('domashniiy')
    print translit('pirog')

    # for item in w:
    # item = get_normal(item)
    #     print item[0][0], item[0][1]
