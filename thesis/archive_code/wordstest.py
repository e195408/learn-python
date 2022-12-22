# モジュールのインポート
import os
import pathlib
import unicodedata

import MeCab as mc
import re

import numpy as np



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


def mecab_analysis(text):
    """
    MeCabをつかって単語を切り出してリストに詰める関数．
    可視化して意味がありそうな単語を抽出するために品詞は名詞だけ（あるいは名詞、動詞、形容詞、副詞）に限定．
    """
    mecab = mc.Tagger('-Ochasen')
    t = mc.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/')
    text = unicodedata.normalize('NFC', text)

    node = mecab.parseToNode(text)
    #     print(node)
    words = []
    while(node):
        #         print(node.surface, node.feature)
        if node.surface != "":  # ヘッダとフッタを除外
            word_type = node.feature.split(",")[0]
            # 名詞だけをリストに追加する
            if word_type in ["名詞"]:
                words.append(node.surface)  # node.surface は「表層形」
            # 動詞（の原型），形容詞，副詞もリストに加えたい場合は次の２行を有効にする
            if word_type in [ "動詞", "形容詞","副詞"]:
                words.append(node.feature.split(",")[6]) # node.feature.split(",")[6] は形態素解析結果の「原型」
        node = node.next
        if node is None:
            break
    StrWords = "".join([str(_)for _ in words])
    return StrWords


def get_DF_from_Filepaths(filepaths, vocab):
    """
    ファイル名のリストを与えて，DFの値を返します．
    DFは索引語が出現する文書数のこと．
    """
    # 辞書の長さと同じ長さで DF を初期化する
    df = np.zeros((len(vocab), 1))

    for filepath in filepaths:
        f = open(filepath, encoding='utf-8')
        raw = f.read()
        text = strip_CRLF_from_Text(raw) # 改行を削除
        words = mecab_analysis(text)  # 名詞だけのリストを生成
        for s in set(words):  # 単語の重複を除いて登場した単語を数える
            df[vocab.index(s), 0] += 1
    return df


def get_TF_from_Filepaths(filepaths, vocab):
    """
    ファイル名のリストを与えて，TFの値を返します．
    TFは索引語の出現頻度のこと．
    """
    n_docs = len(txtList)
    n_vocab = len(vocab)

    # 行数 = 登録辞書数， 列数 = 文書数 で tf を初期化する
    tf = np.zeros((n_vocab, n_docs))

    for filepath in filepaths:
        f = open(filepath, encoding='utf-8')
        raw = f.read()
        text = strip_CRLF_from_Text(raw)
        words = mecab_analysis(text)
        for w in words:
            tf[vocab.index(w), filepaths.index(filepath)] += 1
    return tf


def get_TFIDF_from_TF_DF(tf, df):
    """
    TFとDFを与えて，TF-IDFの値を返します．
    """
    return tf/df


def get_distance_matrix(tfidf):
    """
    tfidf の行列を渡せば，文書間の距離を計算して，行列を返します．
    """
    n_docs = tfidf.shape[1]
    n_words = tfidf.shape[0]
    # 結果を格納する行列を準備（初期化）する
    distance_matrix = np.zeros([n_docs, n_docs])    # 文書数 x 文書数

    for origin in range(n_docs):   # origin : 比較元文書
        tmp_matrix = np.zeros([n_words, n_docs])           # 単語数 x 文書数

        # 比較元文書のTFIDFを取得する
        origin_tfidf = tfidf[0:n_words, origin]

        # 各要素の二乗誤差を取る
        for i in range(n_docs):    # 列のループ    0:5 （文書数）
            for j in range(n_words):   # 行のループ   0:20 （単語数）
                tmp_matrix[j, i] = (tfidf[j, i] - origin_tfidf[j])**2

        # 二乗誤差の合計の平方根を計算
        for i in range(n_docs):
            distance_matrix[origin, i] = np.sqrt(tmp_matrix.sum(axis=0)[i])
    return distance_matrix


p_temp = pathlib.Path('thesis/miyaken_txt')
txtList = list(p_temp.glob('a101404_uematsu.txt'))
for txtFile in txtList:
    with open(txtFile, mode='r') as f:
        raw = f.read()
        #中身をそのまま表示する
        # print(raw)
        # 改行を削除して表示する
        text = strip_CRLF_from_Text(raw)
        # print(text)
        file_name = os.path.splitext(os.path.basename(txtFile))[0]
        with open('thesis/miyaken_output/' + file_name + '.txt', 'w') as txtf:
            words = mecab_analysis(text)
            print(words)
            txtf.write(words)
            txtf.close()

### Mecabによる形態素解析
### すべての文書を分かち書きをして，名詞だけ取り出したリストを作成する

vocab = sorted(set(words))

df = get_DF_from_Filepaths(txtList, vocab)
tf = get_TF_from_Filepaths(txtList, vocab)
tfidf= get_TFIDF_from_TF_DF(tf, df)

distance_matrix = get_distance_matrix(tfidf)

for i in range(len(vocab)):
    print(vocab[i], tf[i])