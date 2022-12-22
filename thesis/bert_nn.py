# BERTの日本語モデル
MODEL_NAME = 'cl-tohoku/bert-base-japanese-whole-word-masking'

#トークナイザとモデルのロード
tokenizer = BertJapaneseTokenizer.from_pretrained(MODEL_NAME)
model = BertModel.from_pretrained(MODEL_NAME)
model = model.cuda()

#各データの形式を整える
max_length = 256

sentence_vectors = []
labels = []
for i in range(len(df)):
    # 記事から文章を抜き出し符号化を行う
    lines = df.iloc[i,3].splitlines()
    text = '\n'.join(lines)
    encoding = tokenizer(
        text,
        max_length = max_length,
        padding = 'max_length',
        truncation = True,
        return_tensors = 'pt'
    )
    encoding = {k: v.cuda() for k, v in encoding.items()}
    attention_mask = encoding['attention_mask']

    #文章ベクトルを計算
    with torch.no_grad():
        output = model(**encoding)
        last_hidden_state = output.last_hidden_state
        averaged_hidden_state =(last_hidden_state*attention_mask.unsqueeze(-1)).sum(1)/attention_mask.sum(1,keepdim=True)

        #文章ベクトルとラベルを追加
    sentence_vectors.append(averaged_hidden_state[0].cpu().numpy())
    label = df.iloc[i,4]
    labels.append(label)

#ベクトルとラベルをnumpy.ndarrayにする
sentence_vectors = np.vstack(sentence_vectors)
labels = np.array(labels)
