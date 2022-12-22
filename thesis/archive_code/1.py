import codecs
import os
import pathlib
from collections import Counter
from math import log
import re

import MeCab

tagger = MeCab.Tagger('-Ochasen')
# define stop word
stop_word_list = ['の', 'よう', 'それ', 'もの', 'ん', 'そこ', 'うち', 'さん', 'そう', 'ところ',
                  'これ', '-', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']


def get_filename_list():
    p_temp = pathlib.Path('thesis/miyaken_txt')
    txtList = list(p_temp.glob('*.txt'))
    filename_list = []
    for txtFile in txtList:
        print(txtFile)
        filename_list.append(txtFile)
        with open(txtFile, mode='r', encoding='utf-8') as f:
            raw = f.read()
            # 改行と空白を削除して表示する
            text = strip_CRLF_from_Text(raw)

    return filename_list


def strip_CRLF_from_Text(text):
    """
    テキストファイルの改行，タブを削除する．
    改行前後が日本語文字の場合は改行文字やタブ文字を削除する．
    それ以外はスペースに置換する．
    """
    # 改行前後の文字が日本語文字の場合は改行を削除する
    plaintext = re.sub('([ぁ-んー]+|[ァ-ンー]+|[\\u4e00-\\u9FFF]+|[ぁ-んァ-ンー\\u4e00-\\u9FFF]+)(\n)([ぁ-んー]+|[ァ-ンー]+|[\\u4e00-\\u9FFF]+|[ぁ-んァ-ンー\\u4e00-\\u9FFF]+)',
                       r'\1\3',
                       text)
    # 改行前後の文字が日本語文字の場合は空白を削除する
    plaintext = re.sub('([ぁ-んー]+|[ァ-ンー]+|[\\u4e00-\\u9FFF]+|[ぁ-んァ-ンー\\u4e00-\\u9FFF]+)(\s)([ぁ-んー]+|[ァ-ンー]+|[\\u4e00-\\u9FFF]+|[ぁ-んァ-ンー\\u4e00-\\u9FFF]+)',
                       r'\1\3',
                       plaintext)
    # 残った改行とタブ記号はスペースに置換する
    plaintext = plaintext.replace('\n', ' ').replace('\t', ' ')
    return plaintext


def get_word_counter(filename):
    filepath = 'thesis/miyaken_output/' + filename
    with codecs.open(filepath, 'r', encoding='utf-8') as fp:
        word_counter = Counter()
        text = fp.read()
        text_lines = text.split('\n')
        for text_line in text_lines:
            node = tagger.parseToNode(text_line)
            while node:
                word_type = node.feature.split(',')[0]
                if (word_type == '名詞') and (len(node.surface) != 0) \
                        and (not(node.surface in stop_word_list)):
                    word_counter[node.surface] += 1
                node = node.next
    return word_counter


def get_tf_dict(word_counter):
    tf_dict = {}
    word_total = sum(word_counter.values())
    for word, count in word_counter.items():
        tf_dict[word] = count/word_total
    return tf_dict


def get_idf_dict(file_word_counter, targetname):
    word_list = file_word_counter[targetname].keys()
    filename_list = file_word_counter.keys()
    idf_dict = {}
    for word in word_list:
        word_count = 0
        for filename in filename_list:
            if word in file_word_counter[filename].keys():
                word_count += 1
        idf_dict[word] = log(len(filename_list)/word_count)+1
    return idf_dict


if __name__ == '__main__':
    filename_list = get_filename_list()
    file_word_counter = Counter()
    # get word_dict
    for filename in filename_list:
        file_word_counter[filename] = get_word_counter(filename)
    # get tf and idf score
    file_tf_dict = {}
    file_idf_dict = {}
    for filename in filename_list:
        file_tf_dict[filename] = get_tf_dict(file_word_counter[filename])
        file_idf_dict[filename] = get_idf_dict(file_word_counter, filename)
    # get tf-idf score
    file_tfidf_dict = {}
    for filename in filename_list:
        tfidf_dict = {}
        for word in file_word_counter[filename].keys():
            tfidf_dict[word] = file_tf_dict[filename][word] * \
                               file_idf_dict[filename][word]
        file_tfidf_dict[filename] = tfidf_dict
    # print tf-idf score top 10 words
    for filename in filename_list:
        print('filename:{0}'.format(filename))
        tfidf_sorted = sorted(file_tfidf_dict[filename].items(),
                              key=lambda x: x[1], reverse=True)
        print('word number:{0}'.format(len(tfidf_sorted)))
        print('number\tword\t\tscore')
        for i in range(0, 10):
            print('{0}\t{1}\t\t{2}'.format(
                i+1, tfidf_sorted[i][0], tfidf_sorted[i][1]))
        print()
    # get file_string_dict
    file_string_dict = {}
    for filename in filename_list:
        string = ''
        tfidf_total = sum(file_tfidf_dict[filename].values())
        for word, score in file_tfidf_dict[filename].items():
            rate = (10000*score)//tfidf_total
            if rate >= 1.0:
                string += (word+' ')*int(rate)
        file_string_dict[filename] = string