import pathlib
import re

from collections import defaultdict


def sentences_generator():
    sentences = []
    morphs = []
    meca_path = pathlib.Path('thesis/miyaken_output')
    meca_list = list(meca_path.glob('*.txt'))
    # print(meca_list)
    for meca in meca_list:
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

    return sentences


def countup_words(sentences):
    ans = defaultdict(int)  # defaultdict→値の初期値が0でセットされる
    for sentence in sentences:
        for morph in sentence:
            # if morph['pos'] != '記号':
            if morph['pos'] == '名詞':
                ans[morph['base']] += 1  # 単語数の更新(初登場の単語であれば0→1に)
    # print(ans.items())
    ans = sorted(ans.items(), key=lambda x: x[1], reverse=True)
    # 第一引数→ソートの対象リスト
    # 第二引数→ソートの対象項目
    # 第三引数→reverse=True（降順）， reverse=false（昇順）

    # 確認
    for w in ans[:100]:
        print(w)

    return ans


def main():
    sentences = sentences_generator()
    ans = countup_words(sentences)



if __name__ == "__main__":
        main()
