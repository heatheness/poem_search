# -*- coding: utf-8 -*-
"""
Module is responsible for eternal waiting for user's
input, representation of this input and form list of search results

"""

from search import process_req

__author__ = 'mayns'

prompt = u"Hey there! I'm ready to process your request\n>> "


def result_formatter(results):

    """
    :param results: list of poems
    :type results: list
    :rtype: str
    """
    if not results:
        return u'No results for your request', u'Ups :)'

    l_results = [u'\n- {} -\n{}\n'.format(res[0]+1, res[1]) for res in results]
    stats = u'----\nTotal: {}\nIndexes: {}\n----'.format(len(results), ', '.join([str(r[0]+1) for r in results]))
    return l_results, stats

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
    formatted_res = result_formatter(result)
    if isinstance(formatted_res[0], list) and len(formatted_res[0]) > 10:
        print u''.join(formatted_res[0][:10])
        i = 10
        print u'RESULTS: {}/{}'.format(i, len(formatted_res[0]))
        print formatted_res[1]
        while True:
            further = raw_input(u'Enter any key for more, q to start another query\n>> ').decode(encoding='utf-8')
            if further == u'q':
                break
            else:
                if len(formatted_res[0][i:]) > 10:
                    print u''.join(formatted_res[0][i:i+10])
                    i += 10
                    print u'RESULTS: {}/{}'.format(i, len(formatted_res[0]))
                    print formatted_res[1]
                else:
                    # print 'breaking'
                    print u''.join(formatted_res[0][i:])
                    break
    else:
        print u''.join(formatted_res[0])
    print formatted_res[1]
