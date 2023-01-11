import collections
import csv
import pathlib
import re
import codecs
import os
from collections import Counter
from math import log

from collections import defaultdict

import gensim as gensim
import numpy as np

# モデルのパス
modelPath = "thesis/model.vec"

# モデルのロード
model = gensim.models.KeyedVectors.load_word2vec_format(modelPath, binary=False)

stop_word_list = ['の', 'よう', 'それ', 'もの', 'ん', 'そこ', 'うち', 'さん', 'そう', 'ところ',
                  'これ', '-', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十','こと','*\n']


def get_filename_list():
    meca_path = pathlib.Path('thesis/miyaken_output')
    meca_list = list(meca_path.glob('*.txt'))
    return meca_list


def sentences_generator(meca):
    sentences = []
    morphs = []
    # meca_path = pathlib.Path('thesis/miyaken_output')
    # meca_list = list(meca_path.glob('*.txt'))
    # print(meca_list)
    # for meca in meca_list:
    with open(meca, mode='r') as f:
        for line in f:
            # print(line)
            if line != 'EOS\n':  # 文末以外：形態素解析情報を辞書型に格納して形態素リストに追加
                fields = line.split('\t')
                # print(fields)
                if len(fields) != 2 or fields[0] == '':  # 文頭以外の空白と改行文字はスキップ
                    # len(fields) != 2 → ['\n']
                    # fields[0] == '' → ['', '記号,一般,*,*,*,*,*\n']
                    continue
                else:
                    attr = fields[1].split(',')
                    morph = {'surface': fields[0], 'base': attr[6], 'pos': attr[0], 'pos1': attr[1]}
                    morphs.append(morph)
            else:  # 文末：形態素リストを文リストに追加
                sentences.append(morphs)
                morphs = []
            # with open(filename, mode='r') as f:
            #     for line in f:  # 1行ずつ読込
    # # 確認
    # for morph in sentences:
    #     print(morph)
    # print(sentences)

    return sentences


def countup_words(sentences):
    ans = defaultdict(int)  # defaultdict→値の初期値が0でセットされる
    for sentence in sentences:
        for morph in sentence:
            # if morph['pos'] != '記号':
            if (morph['pos'] == '名詞') and (not(morph['base'] in stop_word_list)):
                ans[morph['base']] += 1  # 単語数の更新(初登場の単語であれば0→1に)
    # print(ans.items())
    # ans = sorted(ans.items(), key=lambda x: x[1], reverse=True)
    # # 第一引数→ソートの対象リスト
    # # 第二引数→ソートの対象項目
    # # 第三引数→reverse=True（降順）， reverse=false（昇順）
    #
    # # 確認
    # for w in ans[:100]:
    #     print(w)

    return ans


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


def text_vector(tfidf_sorted_word):
    _sv = []
    unknowns = []
    for w in tfidf_sorted_word:
        try:
            wv = model[w]
            _sv.append(wv)
        except KeyError:
            if w not in unknowns:
                unknowns.append(w)
    # if _sv.shape[0]>0:
    #     return np.array([np.average(_sv, axis=0)])
    # else:
    #     print('Ignore sentence' , tfidf_sorted_word)
    vector = np.array(np.average(_sv))

    return vector


def get_namelab_from_path(filename_path):
    filename_path = str(filename_path)
    target1 = 'thesis/miyaken_output/'
    idx1 = filename_path.find(target1)
    target2 = '.txt'
    idx2 = filename_path.find(target2)
    filename_plane = filename_path[idx1+len(target1):idx2]
    # print(filename)

    sep = '_'
    name = filename_plane.split(sep)

    lab = name[0]
    filename_plane = name[1]

    return lab, filename_plane


def main():
    filename_list = get_filename_list()
    file_word_counter = Counter()
    # sentences = sentences_generator(filename_list)
    # ans = countup_words(sentences)
    file_tf_dict = {}
    file_idf_dict = {}
    file_tfidf_dict = {}
    file_vector_dict = {}
    for filename in filename_list:
        sentences = sentences_generator(filename)
        file_word_counter[filename] = countup_words(sentences)
        file_tf_dict[filename] = get_tf_dict(file_word_counter[filename])
        file_idf_dict[filename] = get_idf_dict(file_word_counter, filename)
        tfidf_dict = {}
        for word in file_word_counter[filename].keys():
            tfidf_dict[word] = file_tf_dict[filename][word] * \
                               file_idf_dict[filename][word]
        file_tfidf_dict[filename] = tfidf_dict
        # print(file_tfidf_dict)
        # 特徴語リスト＝file_tfidf_dict (辞書型）

    for filename in filename_list:
        print('filename:{0}'.format(filename))
        # print(file_tfidf_dict[filename])
        tfidf_sorted = sorted(file_tfidf_dict[filename].items(),
                              key=lambda x: x[1], reverse=True)
        print('word number:{0}'.format(len(tfidf_sorted)))
        print('number\tword\t\tscore')
        for i in range(0, 10):
            print('{0}\t{1}\t\t{2}'.format(
                i+1, tfidf_sorted[i][0], tfidf_sorted[i][1]))

        # 特徴的な語上位リスト = tfidf_sorted（list型）
        # print(type(tfidf_sorted))

        tfidf_sorted_list = np.array(tfidf_sorted)
        tfidf_sorted_wordlist = list(map(lambda x:x[0], tfidf_sorted_list))
        # print(tfidf_sorted_word)
        top_word = tfidf_sorted_wordlist[:700]
        # print(len(top_word))
        # 特徴語リスト上位700 = top_word（リスト）

        lab, filename_plane = get_namelab_from_path(filename)
        with open('thesis/miyaken_tfidf/' + filename_plane + '.txt', 'w', encoding='utf-8') as output_file:
            for x in tfidf_sorted_list:
                output_file.write(str(x) + "\n")
            output_file.close()

        file_vector_dict[filename] = text_vector(top_word)

    HEADER = ['name', 'lab', 'vector']
    with open('thesis/thesis_vector.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)

        print(file_vector_dict)

        for filename in filename_list:
            lab, filename_plane = get_namelab_from_path(filename)
            print(filename)
            print('lab:{0}'.format(lab))
            print('name:{0}'.format(filename_plane))

            vector = file_vector_dict[filename]

            print('vector:{0}'.format(vector))
            print()

            row =[filename_plane, lab, vector]
            writer.writerow(row)



if __name__ == "__main__":
    main()
