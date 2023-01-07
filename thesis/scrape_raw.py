# scrape_class_basic.pyで取得した授業詳細ページのURLから講義情報を取得する

import csv
import os
import pathlib
import time
from matplotlib.pyplot import cla
import requests
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import mecab_nn


def daterange(_start, _end):
    for n in range((_end - _start).days):
        yield _start + timedelta(n)

def scrapeSessions():
    # csvのヘッダーを設定
    HEADER = ['name', 'grade', 'class_no', 'semester', 'teacher', 'detail']
    # csvファイルを作成
    p_temp = pathlib.Path('output/')
    classesList = list(p_temp.glob('*.csv'))
    # print(classesList)
    for classesFile in classesList:
        # print(classesFile)
        with open(classesFile, 'r', encoding='utf-8') as input_file:
            reader = csv.reader(input_file)
            header = next(input_file)
            # print(reader)

            for name in reader:
                    # print(name)
                    file_name = os.path.splitext(os.path.basename(classesFile))[0]
                    print(file_name)
                    with open('text/' + file_name + '.csv', 'w', encoding='utf-8') as output_file:
                        writer = csv.writer(output_file)
                        writer.writerow(HEADER)
                        time.sleep(1)

                        link = name[1]
                        # リクエストを実行
                        res = requests.get(link)
                        print(res)  # 結果を確認

                        # BeautifulSoupでhtmlのtextのみ抽出
                        soup = BeautifulSoup(res.text, 'html.parser')
                        tr_lists = soup.find_all('table')
                        for i, tr in enumerate(tr_lists):
                            if i<2:
                                continue
                            elif tr.find_all(colspan="3"):
                                contents = tr.find_all(class_="txt12")
                                # print(contents)
                                name1 = name[0]
                                grade = name[2]
                                class_no = name[3]
                                semester = name[4]
                                teacher = name[7]
                                # print(contents[0])

                                detail = mecab_nn.strip_CRLF_from_Text(contents[0].get_text(strip=True))
                                # print(detail)

                                row = [name1, grade, class_no, semester, teacher, detail]
                                print(row)
                                writer.writerow(row)


def remove(str):
    disturbers = ['\n', '\r', '\u3000', '<br>', '<br />', '</br>', '<br/>']
    for disturber in disturbers:
        str = str.replace(disturber, '')
    return str


if __name__ == "__main__":
    scrapeSessions()
