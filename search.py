# -*- coding: utf-8 -*-
"""
Basic module to search for correct response on user's request.
All search logic is here.

"""

from text_utils import clear, get_normal, clear_req
from index import get_index_data, get_poem
from itertools import *
from handle_request import amazing_fun

__author__ = 'mayns'

word_type_scores = {
    u'существительное': 1,
    u'прилагательное': 1,
    u'наречие': 1,
    u'глагол': 1,
    u'причастие': 1,
    u'деепричастие': 1,
    u'числительное': 0.8,
    u'местоимение': 0.8,
    u'частица': 0.2,
    u'союз': 0.2,
    u'предлог': 0.2,
    u'междометие': 0.2,
}


def process_req(req):
    """
    1. Intersection of all occurrences
        - YES -> full search (clean req in clean poem), sort by frequency, add to results and return them
        - NO  -> look for intersection in combinations, sort them with destination scores
    :type req: str | unicode
    :return: list of tuples with index and poem like [(index, poem)...]
    """
    i_result = []
    req_indexes = []
    full_intersection = []
    normal_req = normalize_req(req)
    flatten_variants = [x[0] for x in normal_req]
    
    for word in flatten_variants:
        req_indexes.append(get_index_data(word))
    if req_indexes:
        full_intersection = get_intersection(req_indexes)

    if full_intersection:
        full_hit = full_search(req, list(set(full_intersection)))
        if full_hit:
            sorted_results = cmp_by_frequency(full_hit, req_indexes)
            for i in sorted_results:
                i_result.append(i)
            if len(normal_req) > 3:
                return [(i, get_poem(i)) for i in i_result]

    #yobisearch here appended to oks search
    yobi_res = process_request(req)
    for elem in yobi_res:
        if elem not in i_result:
            i_result.append(elem)
    return [(i, get_poem(i)) for i in i_result]


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


def get_len_score(normalized_req):
    score = 0
    for elem in normalized_req:
        score += word_type_scores[elem[1]]
    return score/len(normalized_req)


def get_pos_score(elem):
    ctr = 0
    for word_id in elem:
        ctr += len(elem[word_id])
    return ctr


def get_identical_words_score(elem):
    positions = elem.values()
    all_combs = product(*positions)
    global_min = None
    for comb in all_combs:
        local_min = max(comb) - min(comb)
        if global_min < local_min or global_min == None:
            global_min = local_min
    return global_min
      

def check_phrase(phrase, normalized_req):
    res_dict = {}

    for word in phrase:
        #w_t is (pid:pos)
        w_t = get_index_data(word)
        for elem in w_t:
            pid = elem[0]
            if pid not in res_dict.keys():
                res_dict[pid] = {word:[elem[1]]}
            elif word in res_dict[pid].values():
                val = res_dict[pid][word]
                val.append(w_t[1])
                res_dict[pid] = {word:val}
    if not res_dict:
        return None

    maxlen = max([len(res_dict[el].keys()) for el in res_dict])
    cands = [pid for pid in res_dict if len(res_dict[pid].keys()) == maxlen]
 
    #elem is ({word:[positions]},len_score,pos_score, identical_words_score)
    result = {}
    for elem in cands:
        to_check = res_dict[elem]
        len_score = get_len_score(normalized_req)
        pos_score = get_pos_score(to_check)
        identical_words_score = get_identical_words_score(to_check)
        result[elem] = (res_dict[elem],len_score,pos_score,identical_words_score)
  
    return result


def normalize_req(req):
    clean_req = clear(req)
    normal_req = [get_normal(w)[0] for w in clean_req if get_normal(w)]
    return normal_req


def process_request(request):
    corrected_req = clear_req(request)
    search_phrases = []
    for r in corrected_req:
        search_phrases.extend(amazing_fun(r))
    # search_phrases = amazing_fun(request)

    result = {}
    #only the most len_scored elem with identical pid remains
    for phrase in search_phrases:
        normalized_req = normalize_req(phrase)
        tmp_res = check_phrase(phrase.split(), normalized_req)
        if not tmp_res:
            continue
        for pid in tmp_res:
            if pid not in result:
                result[pid] = tmp_res[pid]
            elif len(tmp_res[pid][0].keys()) > len(result[pid][0].keys()):
                result[pid] = tmp_res[pid]
    #sort result by len_score, subsort by pos_score, subsort by identical_worts_score
    final_res = sorted(result, key=lambda elem: (result[elem][1], result[elem][2], result[elem][3]), reverse=True)
    return final_res


def get_intersection(indexes):
    sets = []
    for word_indexes in indexes:
        word_set = set([x[0] for x in word_indexes])
        sets.append(word_set)
    intersection = set.intersection(*sets)
    return list(intersection)

if __name__ == u'__main__':
    # process_request(u'стали ждать ответа')
    cmp_by_frequency([129, 5, 141, 160, 162, 35, 37, 44, 51, 59, 62, 79, 91, 111, 122, 126],
                     [[[3, 12], [5, 3], [16, 6], [16, 10], [16, 18], [23, 54], [26, 29], [27, 25], [35, 1],
                       [35, 52], [37, 62], [41, 19], [44, 11], [44, 25], [44, 48], [51, 4], [51, 18], [56, 27],
                       [59, 5], [59, 55], [60, 27], [62, 21], [68, 6], [70, 14], [79, 17], [79, 43], [81, 1],
                       [83, 31], [86, 15], [89, 3], [91, 4], [111, 5], [122, 12], [126, 7], [129, 27],
                       [133, 8], [138, 34], [140, 11], [141, 4], [152, 11], [155, 9], [160, 13], [162, 1],
                       [170, 31], [173, 5], [174, 3], [180, 18]]])
