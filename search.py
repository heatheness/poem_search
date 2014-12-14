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
        - YES -> full search (clean req in clean poem), sort by frequency, add to results and return them
        - NO  -> look for intersection in combinations, sort them with destination scores
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

    full_intersection = get_intersection(req_indexes)

    if full_intersection:
        full_hit = full_search(req, list(set(full_intersection)))
        if full_hit:
            sorted_results = cmp_by_frequency(full_hit, req_indexes)
            for i in sorted_results:
                results.append((i, get_poem(i)))
            return results


def cmp_by_frequency(intersection, indexes):
    results = {}
    for i in intersection:
        results.setdefault(i, 0)
        for j in indexes:
            for k in j:
                results[i] += 1 if k[0] == i else 0
    return [l[0] for l in sorted(zip(results.keys(), results.values()), key=lambda e: e[1], reverse=True)]


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
    # process_request(u'стали ждать ответа')
    cmp_by_frequency([129, 5, 141, 160, 162, 35, 37, 44, 51, 59, 62, 79, 91, 111, 122, 126], [[[3, 12], [5, 3], [16, 6], [16, 10], [16, 18], [23, 54], [26, 29], [27, 25], [35, 1], [35, 52], [37, 62], [41, 19], [44, 11], [44, 25], [44, 48], [51, 4], [51, 18], [56, 27], [59, 5], [59, 55], [60, 27], [62, 21], [68, 6], [70, 14], [79, 17], [79, 43], [81, 1], [83, 31], [86, 15], [89, 3], [91, 4], [111, 5], [122, 12], [126, 7], [129, 27], [133, 8], [138, 34], [140, 11], [141, 4], [152, 11], [155, 9], [160, 13], [162, 1], [170, 31], [173, 5], [174, 3], [180, 18]]])