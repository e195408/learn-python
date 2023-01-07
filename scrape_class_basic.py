# scrape_faculty.pyで取得した学科ごとのURLから授業詳細ページのURLを取得する

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
    # csvのヘッダーを設定
    HEADER = ['name', 'link', 'grade', 'class_no', 'semester', 'hour', 'room', 'teacher', 'memo']
    # csvファイルを作成
    with open('faculty.csv', 'r', encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        header = next(input_file)
        for faculty, link in reader:
            print(faculty, link)
            with open('output/' + faculty + '.csv', 'w', encoding='utf-8') as output_file:
                writer = csv.writer(output_file)
                writer.writerow(HEADER)
                time.sleep(1)
                    
                # リクエストを実行
                url = 'https://portal.u-gakugei.ac.jp/syllabus/'+link
                # print(url)
                res = requests.get(url)
                # print(res)  # 結果を確認

                # BeautifulSoupでhtmlのtextのみ抽出
                soup = BeautifulSoup(res.text, 'html.parser')
                tr_lists = soup.find_all('tr')
                for i, tr in enumerate(tr_lists):
                    if i<2:
                        continue
                    elif tr.has_attr("data-href"):
                        contents = tr.find_all('td') 
                        # print(contents)
                        name = contents[1].text
                        link = tr['data-href']
                        grade = contents[2].text
                        class_no = contents[3].text
                        semester = contents[4].text
                        hour = contents[5].text
                        room = contents[6].text
                        teacher = contents[7].text
                        memo = contents[8].text
                        
                        row = [name, link, grade, class_no, semester, hour, room, teacher, memo]
                        writer.writerow(row)
                        
                        
                            
                    

def remove(str):
    disturbers = ['\n', '\r', '\u3000', '<br>', '<br />', '</br>', '<br/>']
    for disturber in disturbers:
        str = str.replace(disturber, '')
    return str


if __name__ == "__main__":
    scrapeSessions()
