# シラバスから学科ごとのシラバスページURLを取得する

import csv
import time
from matplotlib.pyplot import cla
import requests
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta


def daterange(_start, _end):
    for n in range((_end - _start).days):
        yield _start + timedelta(n)


def scrapeSessions():
    # リクエスト先のURL（日付部分は繰り返しの中で結合）
    url = 'https://portal.u-gakugei.ac.jp/syllabus/'
    
    # 勉強会一覧を取得
    HEADER = ['faculty', 'link']
    # csvファイルを作成
    with open('faculty.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        time.sleep(1)
            
        # リクエストを実行
        res = requests.get(url)
        print(res)  # 結果を確認

        # BeautifulSoupでhtmlのtextのみ抽出
        soup = BeautifulSoup(res.text, 'html.parser')
        # faculties = {}
        for _, elem in enumerate(soup.find_all("div", id="tab1")):
            li_list = elem.find_all('a', href=re.compile("tab_kamoku.php"))
            for _, li in enumerate(li_list):
                department = li.text
                link = li['href']
                
                # 情報をcsvに保存
                row = [department, link]
                print(row)
                writer.writerow(row)
            

def remove(str):
    disturbers = ['\n', '\r', '\u3000', '<br>', '<br />', '</br>', '<br/>']
    for disturber in disturbers:
        str = str.replace(disturber, '')
    return str


if __name__ == "__main__":
    scrapeSessions()
