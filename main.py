# -*- coding: utf-8 -*-
"""
Module is responsible for eternal waiting for user's
input, representation of this input and form list of search results

"""

from search import process_req
import json
__author__ = 'mayns'

prompt = u"Hey there! I'm ready to process your request\n>> "


def result_formatter(results):

    """
    :param results: list of poems
    :type results: list
    :rtype: str
    """
    if not results:
        return u'No results for your request'

    str_results = [u'\n- {} -\n{}\n'.format(res[0]+1, res[1]) for res in results]
    stats = u'----\nTotal: {}\nIndexes: {}\n----'.format(len(results), ', '.join([str(r[0]+1) for r in results]))
    return u''.join(str_results), stats

# print prompt
# x = lambda: raw_input().decode(encoding='utf-8')

while True:
    req = raw_input(prompt).decode('utf-8', 'ignore')
    # sentinel = ''
    # req = '\n'.join(iter(x, sentinel))
    if req == u'exit':
        print u'Bye!'
        break
    result = process_req(req)
    for r in result_formatter(result):
        print r
