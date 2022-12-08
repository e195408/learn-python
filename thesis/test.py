import MeCab as mc

mecab = mc.Tagger('-Ochasen')
sent = "自然言語処理の基本を説明します"
print(mecab.parse(sent))

#mecab-ipa-NEologd 辞書を標準辞書に設定している

