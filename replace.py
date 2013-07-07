#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

def file_to_string(filepath):
    f = open(filepath, 'r')

    text = ''
    for line in f:
        text += line

    f.close()

    return text

def extract_text(text):
    # %@begin{label}
    #    置換に使う文章   ->   ('label', '置換に使う文章')
    # %@end{label}

    pat = re.compile(r'%@begin\{(.+?)\}(?=(.*?)%@end\{\1\})', re.S)

    return pat.findall(text)

def to_text_replace_table(tuples):
    # ('label', '置換に使う文章')   ->   ('@[label]', '置換に使う文章')

    replace_table = {}

    for t in tuples:
        replace_table['@[' + t[0] + ']'] = remove_comment(t[1])

    return replace_table

def extract_reference(text):
    # \bibitem[表示文字列]{label} -> ('表示文字列', 'label')

    pat = re.compile(r'\\bibitem\[(.+?)\]\{(.+?)\}', re.S)

    return pat.findall(normalize_text(text))

def to_reference_replace_table(tuples):
    # ('表示文字列', 'label')   ->   ('\cite{label}', '[表示文字列]')
    replace_table = {}

    for t in tuples:
        replace_table['\cite{' + t[1] + '}'] = '[' + t[0] + ']'

    return replace_table

def normalize_text(text):
    return remove_multiple_space(remove_newline_char(text))

def remove_newline_char(text):
    return text.replace('\n', '')

def remove_multiple_space(text):
    return re.compile('  [ ]*').sub(' ', text)

def remove_comment(text):
    return re.compile('[^\\\](%.*?$)').sub(' ', text)

def replace(text, replace_table):
    for before, after in replace_table.iteritems():
        text = text.replace(before, after)

    return text

def replace_text(src_text, dest_text):
    replace_table = to_text_replace_table(extract_text(src_text))

    return replace(dest_text, replace_table)

def replace_reference(src_text, dest_text):
    replace_table = to_reference_replace_table(extract_reference(src_text))

    return replace(dest_text, replace_table)

# for debug
def print_dictionary(dic):
    for key, value in dic.iteritems():
        print key +  '=>' + value

#
# main
#

argv = sys.argv
argc = len(argv)

if not (argc == 3 or argc == 4):
    print 'Usage: ' + argv[0] + ' main.tex response.tex [output.tex]'
    quit()

output_file_name = 'auto-' + argv[2]
if argc == 4:
    output_file_name = argv[3]


context_replaced_marker = replace_text(file_to_string(argv[1]), file_to_string(argv[2]))

output_file = open(output_file_name, 'w')
output_file.write(context_replaced_marker)
output_file.close()

# end of file
