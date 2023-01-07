import csv
import os
import pathlib
import unicodedata

import mecab_nn

def morphological():
    p_temp = pathlib.Path('text/')
    classesList = list(p_temp.glob('*.csv'))
    for classesFile in classesList:
        with open(classesFile, mode='r', encoding='utf-8') as input_file:
            reader = csv.reader(input_file)
            # header = next(input_file)
            print(classesFile)

            for row in reader:
                # print(row)
                raw = row[5]
                text = mecab_nn.strip_CRLF_from_Text(raw)
                text = unicodedata.normalize('NFC', text)
                print(row[0])
                name = row[0].replace('/', ' ')

                with open('thesis/classes/' + name + '_' + row[4] + '.txt', 'w') as txtf:
                    txtf.write(mecab_nn.my_mecab(text))
                    txtf.close()


if __name__ == "__main__":
    morphological()

