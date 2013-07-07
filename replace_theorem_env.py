#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

def replace_all(text):
    text = replace_definition(text)
    text = replace_theorem(text)
    text = replace_lemma(text)
    text = replace_corollary(text)
    text = replace_assumption(text)

    text = replace_proof(text)

    text = replace_proposition(text)
    text = replace_example(text)

    return text

def replace_theorem_env(text, env_name, lparen, rparen):
    before = ''\
        + r'\\begin\{' + env_name + r'\}\[(.+?)\].*?'\
        + r'\\label\{(.+?)\}'\
        + r'\n*(.+?)\n*'\
        + r'\\end\{' + env_name + r'\}'

    after  = ''\
        + r'\\begin{flushleft}\n'\
        + r'{\\bf ' + lparen + r'\\ref{\2}' + rparen + r'（\1）}\n'\
        + r'\3'\
        + r'\\end{flushleft}'

    return re.compile(before, re.S).sub(after, text)

def replace_definition(text):
    return replace_theorem_env(text, 'definition', '【', '】')

def replace_theorem(text):
    return replace_theorem_env(text, 'theorem', '［', '］')

def replace_lemma(text):
    return replace_theorem_env(text, 'lemma', '［', '］')

def replace_corollary(text):
    return replace_theorem_env(text, 'corollary', '（', '）')

def replace_assumption(text):
    return replace_theorem_env(text, 'assumption', '［', '］')

def replace_proof(text):
    before = ''\
        + r'\\begin\{proof\}'\
        + r'\n*(.+?)\n*'\
        + r'\\end\{proof\}'

    after  = ''\
        + r'\\begin{flushleft}\n'\
        + r'{\\bf《証明》}\n'\
        + r'\1'\
        + r'\\end{flushleft}'

    return re.compile(before, re.S).sub(after, text)

def replace_no_caption_theorem_env(text, env_name, lparen, rparen):
    before = ''\
        + r'\\begin\{' +env_name + r'\}.*?'\
        + r'\\label\{(.+?)\}'\
        + r'\n*(.+?)\n*'\
        + r'\\end\{' + env_name + r'\}'

    after  = ''\
        + r'\\begin{flushleft}\n'\
        + r'{\\bf' + lparen + r'\\ref{\1}' + rparen + r'}\n'\
        + r'\2'\
        + r'\\end{flushleft}'

    return re.compile(before, re.S).sub(after, text)

def replace_example(text):
    return replace_no_caption_theorem_env(text, 'example', '〔', '〕')

def replace_proposition(text):
    return replace_no_caption_theorem_env(text, 'proposition', '〈', '〉')

#
# main
#
argv = sys.argv
argc = len(argv)

if not (argc == 2 or argc == 3):
    print 'Usage: ' + argv[0] + ' main.tex [output.tex]'
    quit()

input_file_name = argv[1]
output_file_name = 'output.tex'
if (argc == 3):
    output_file_name = argv[2]

input_file_context = open(input_file_name, 'r').read()
output_file_context = replace_all(input_file_context)

output_file = open(output_file_name, 'w')
output_file.write(output_file_context)
output_file.close()
