# モジュールのインポート
import os
import pathlib
import unicodedata

import MeCab as mc
import re

import numpy as np


def my_mecab(text):
    mecab = mc.Tagger('-Ochasen')
    text = unicodedata.normalize('NFC', text)

    p_temp = pathlib.Path('thesis/miyaken_output')
    txtList = list(p_temp.glob('*.txt'))
    for txtFile in txtList:
        print(txtFile)
        with open(txtFile, mode='r', encoding='utf-8') as f:
            raw = f.read()
            # 改行と空白を削除して表示する
            text = strip_CRLF_from_Text(raw)
            my_mecab(text)

    with open('/Users/narasakinayu/ghq/github.com/e195408/learn-python/thesis/miyaken_output/miyaken_output', mode='w') as f:
        f.write(mecab.parse(text))


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


p_temp = pathlib.Path('thesis/miyaken_txt')
txtList = list(p_temp.glob('*.txt'))
for txtFile in txtList:
    print(txtFile)
    with open(txtFile, mode='r', encoding='utf-8') as f:
        raw = f.read()
        # 改行と空白を削除して表示する
        text = strip_CRLF_from_Text(raw)
        mecab = mc.Tagger('-Ochasen')
        text = unicodedata.normalize('NFC', text)
        with open(txtFile, mode='w') as d:
            d.write(mecab.parse(text))

