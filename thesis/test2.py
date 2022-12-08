# モジュールのインポート
import os.path
import pathlib

import MeCab as mc
import re


def my_mecab(text):
    mecab = mc.Tagger()
    # mecab = mc.Tagger('d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/')
    return mecab.parse(text)


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
    # 残った改行とタブ記号はスペースに置換する
    plaintext = plaintext.replace('\n', ' ').replace('\t', ' ')
    return plaintext


p_temp = pathlib.Path('thesis/miyaken_txt')
txtList = list(p_temp.glob('*.txt'))
for txtFile in txtList:
    with open(txtFile, mode='r') as f:
        raw = f.read()
        #中身をそのまま表示する
        print(raw)
        # 改行を削除して表示する
        text = strip_CRLF_from_Text(raw)
        print(text)
        file_name = os.path.splitext(os.path.basename(txtFile))[0]
        with open('thesis/miyaken_output/' + file_name + '.txt', 'a') as txtf:
            txtf.write(my_mecab(text))
            txtf.close()

