# -*- coding: utf-8 -*-
"""
Basic module to search for correct response on user's request.
All search logic is here.

"""

from text_utils import clear, get_normal
from index import get_index_data, get_poem
from itertools import *

__author__ = 'mayns'


def process_request(req):
    """
    1. Intersection of all occurrences
    2. YES -- full search (clean req in clean poem)
    :type req: str | unicode
    :return: list of tuples with index and poem like [(index, poem)...]
    """
    results = []
    req_indexes = []

    clean_req = clear(req)
    normal_req = [get_normal(w)[0] for w in clean_req]
    flatten_variants = [x[0] for x in normal_req]

    for word in flatten_variants:
        req_indexes.append(get_index_data(word))

    intersection = get_intersection(req_indexes)

    if intersection:
        full_hit = full_search(req, list(set(intersection)))
        if full_hit:
            for i in full_hit:
                results.append((i, get_poem(i)))
            return results


def full_search(req, indexes):
    clean_req = u' '.join(clear(req))
    result_indexes = []
    for index in indexes:
        poem = get_poem(index)
        clean_poem = u' '.join(clear(poem))
        if clean_req in clean_poem:
            result_indexes.append(index)
    return result_indexes


def get_req_variants(req):

    clean_req = clear(req)
    normal_req = [get_normal(w) for w in clean_req]
    flatten_varinats = []

    for n in normal_req:
        flatten_varinats.append([x[0] for x in n])

    variants = product(*flatten_varinats)
    return list(variants)


# def full_search(req, indexes):
#     for index in indexes:
#         poem = get_poem(index)
#         poem_variants = get_req_variants(poem)
#         poem_variants = [u' '.join(p) for p in poem_variants]
#         for variant in poem_variants:
#             if req in variant:
#                 return req, variant
#     return


def get_intersection(indexes):
    sets = []
    for word_indexes in indexes:
        word_set = set([x[0] for x in word_indexes])
        sets.append(word_set)
    intersection = set.intersection(*sets)
    return list(intersection)

if __name__ == u'__main__':
    process_request(u'стали ждать ответа')