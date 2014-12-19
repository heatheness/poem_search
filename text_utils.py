# -*- coding: utf-8 -*-

"""
Module contains basic functions for handling text
-- clear_request
-- clear
-- get_normal
-- translit
-- keymap

"""

import pymorphy2
import re
from itertools import product

__author__ = 'nyash myash'

delete = re.compile(u'[^а-яА-Я\-ёЁ0-9a-zA-Z]+?', re.UNICODE)
delete2 = re.compile(u"[^а-яА-Я\-ёЁ0-9a-zA-Z§±\[{}\]`~,<.>;']+?", re.UNICODE)
clr = re.compile(r'\s+', re.UNICODE)
morph = pymorphy2.MorphAnalyzer()   # this is out of function for speed increasing


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
    :type s: unicode
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

    for i in xrange(len(s)):
        s[i] = yo_replace(s[i])

    return s


def clear_req(s):
    from handle_request import corrected_spell

    base = u"qwertyuiop[]asdfghjkl;'\zxcvbnm,.§`;'\,./{}|?~±<>"
    s = s.lower()
    s = delete2.sub(' ', s)
    s = clr.sub(u' ', s).strip()
    s = s.replace(u' - ', u' ')
    s = s.split()

    flat_variants = []
    for i in xrange(len(s)):
        word = s[i]
        flag = 1
        for j in word:
            if j not in base:
                flag = 0
                break
        if flag:
            word = keymap(s[i])
            # try:
            #     word_translit = translit(s[i])
            # except KeyError:
            #     flag = 0
        spells = [word]
        spells.extend(corrected_spell(word))
        # if flag:
        #     spells.append(word_translit)
        #     spells.extend(corrected_spell(word_translit))

        flat_variants.append(spells)

    variants = product(*flat_variants)
    variants = list(variants)
    variants = map(lambda req: clear(req), [u' '.join(list(v)) for v in variants])
    variants = [u' '.join(list(v)) for v in variants]
    return list(set(variants))



def get_normal(word):
    """
    :param word: unicode string
    :type word: str
    :return: list of tuples containing normal form and part of speech
    f.i. [('стать', 'глагол'), ('сталь', 'существительное')]
    :rtype: list
    """

    global morph

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


def translit(word):
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
        u"'": u'ь',
        u'yu': u'ю',
        u'ya': u'я'
    }

    translit = []
    keys = base.keys()
    l = len(word)
    i = 0
    while i < l:
        if i + 3 <= l and word[i:i + 3] in keys:
            k = i + 3
        elif i + 2 <= l and word[i:i + 2] in keys:
            k = i + 2
        else:
            k = i + 1
        translit.append(base[word[i:k]])
        i += k - i
    return ''.join(translit)


def keymap(word):

    """
    :param word: unicode word typed with keybord lang (ru word with en keybord)
    :type word: str
    :return: ru word
    :rtype: str
    """
    base = {
        u'q': u'й',
        u'w': u'ц',
        u'e': u'у',
        u'r': u'к',
        u't': u'е',
        u'y': u'н',
        u'u': u'г',
        u'i': u'ш',
        u'o': u'щ',
        u'p': u'з',
        u'[': u'х',
        u']': u'ъ',
        u'a': u'ф',
        u's': u'ы',
        u'd': u'в',
        u'f': u'а',
        u'g': u'п',
        u'h': u'р',
        u'j': u'о',
        u'k': u'л',
        u'l': u'д',
        u';': u'ж',
        u"'": u'э',
        u'§': u'ч',
        u'z': u'я',
        u'x': u'ч',
        u'c': u'с',
        u'v': u'м',
        u'b': u'и',
        u'n': u'т',
        u'm': u'ь',
        u',': u'б',
        u'.': u'ю',
        u'`': u'ё'
    }

    return u''.join([base[i] for i in word])


if __name__ == '__main__':
    # for i in clear_req(u'mама мыла раму'):
    #     print i
    # for i in clear_req(u'gfgf vj;tn'):
    #     print i
    # for i in clear_req(u'j;tn b r лучшему'):
    #     print i
    # for i in clear_req(u'Hет и точн0'):
    #     print i
    for i in clear_req(u'gkfnmtd yt yjie'):
        print i
        # import timeit
        # start = timeit.default_timer()
        # w = clear(u'Кто-то где-то    и может - --это или-- что-то-  -Ёж- и- ёлочка  куда-то')
        # for item in w:
        #     print item
        # print
        #
        # w = clear(u'0дывлоа 185 0ыоало0ыдлао ыатдло0 8ывла8 длолдао33апт 0статься 03')
        # for item in w:
        #     print item
        # print
        #
        # w = clear(u'60дATь')
        # print w[0]
        # print

        # p = get_normal(u'стали')
        # f = get_normal(u'петь')
        # g = get_normal(u'создавать')
        # u = get_normal(u'творить')
        # q = get_normal(u'исследовать')
        # a = get_normal(u'пробовать')
        # print timeit.default_timer() - start
        # for item in p:
        #     print item[0], item[1]
        #
        # print translit(u'domashniiy')
        # print translit(u'pirog')

        # p = get_normal(u'ожет')
        # for item in p:
        #     print item[0], item[1]

        # w = map(keymap, u'vj;tn b yt vj;tn dczrjt ,sdftn d njv nj dcz b rhfcjnf rhfcbdsq wfgkz b pfrfn e t;f yf gjkejcnhjdt \
        # c otkrjq [jnz cbnj gm`n vjkjrj ,eltn abyfkmysq xfq yf itgjn c]tcn rjrjc gm`n abfkrf hjpjdsq lj;lm'.split())
        # for item in w:
        #     print item

        # for item in w:
        # item = get_normal(item)
        #     print item[0][0], item[0][1]
