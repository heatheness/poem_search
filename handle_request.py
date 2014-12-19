# -*- coding: utf-8 -*-
"""
Module contains basic functions for handling user's request
-- getting synonyms
"""

from urllib import quote
import urllib2
import json
from itertools import *
from text_utils import get_normal, clear

__author__ = 'mayns'

KEY = u'dict.1.1.20141207T200218Z.c01ef3f11cea86bf.3421773cbca3c8c8872988fc567a3815f27c0159'
YA_SYNONYMS = \
    lambda text, lang: u'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={key}&lang=' \
                             u'{lang}&text={text}&ui=ru'.format(key=KEY, lang=lang, text=quote(text.encode('utf-8')))

YA_SPELLER = \
    lambda text: u'http://speller.yandex.net/services/spellservice.json/checkText?text={text}'.format(text=quote(text.encode('utf-8')))


def get_syns(words, lang=u'ru-ru'):
    """
    :type words: list
    :param words: list of tuples from get_normal func
    :rtype: list
    """
    syns_variants = []
    for word in words:
        word_syns = set()
        resp = urllib2.urlopen(YA_SYNONYMS(word[0], lang)).read()
        syns = json.loads(resp).get(u'def')
        if not syns:
            continue

        syns = syns[0].get(u'tr')
        if not syns:
            continue

        for syn in syns:
            if syn.get(u'pos') != word[1] or not syn.get(u'text'):
                continue
            word_syns.add(syn.get(u'text'))
            if syn.get(u'syn'):
                map(lambda x: word_syns.add(x['text']), syn['syn'])
        syns_variants.extend(list(word_syns))

    return syns_variants


def corrected_spell(word):
    corrected = []
    try:
        resp = urllib2.urlopen(YA_SPELLER(word)).read()

    except Exception, ex:
        print u'ex', ex
        return []
    variants = json.loads(resp)

    if not variants:
        return []

    for var in variants:

        if u's' in var:
            corrected.extend(var[u's'])

    return corrected


def amazing_fun(boring_string, lang=u'ru-ru'):

    """

    :param boring_string:
    :type boring_string: unicode
    :return:
    :rtype: list
    """
    variants = []
    raw = clear(boring_string)
    original = [get_normal(w) for w in raw]

    for version in original:
        syns_block = get_syns(version, lang)
        variants.append(syns_block)
    columns = []
    flat_original = []
    for i in xrange(len(original)):
        flat_original.append(map(lambda x: x[0], original[i]))

    for i in xrange(len(original)):
        columns.append(flat_original[i])
        if variants[i]:
            columns[i].extend(variants[i])

    full_variants = product(*columns)
    amazing_variants = [' '.join(list(full_var)) for full_var in list(full_variants)]
    # for var in amazing_variants:
    #     print var
    return amazing_variants

if __name__ == u'__main__':
    amazing_fun(u'па')
    # for c in corrected_spell(u'ингридиенты'):
    #     print c