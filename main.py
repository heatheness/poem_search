# -*- coding: utf-8 -*-
"""
Module is responsible for eternal waiting for user's
input, representation of this input and form list of search results

"""

from search import process_request

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
    return u'\n\n***\n\n'.join(results)

while True:
    req = raw_input(prompt)
    if req == u'exit':
        print u'Bye!'
        break
    result = process_request(req)
    print result_formatter(result)