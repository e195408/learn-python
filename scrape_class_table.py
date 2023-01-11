# scrape_class_basic.pyで取得した授業ごとのURLからシラバスの内容を取得する


import csv
import os
import pathlib
from bs4 import BeautifulSoup
import requests


def get_table_from_url(class_name, url):
    print(class_name, url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    table = soup.find('table', class_='txt12')
    if table==None:
        return None
    td_tags = table.find_all('td')
    td_list = [remove(td.text) for td in td_tags]
    return td_list


def main():
    HEADER = ['name', 'grade', 'class_no', 'semester', 'teacher', 'detail']
    # 学科ごとのファイル一覧を取得
    p_temp = pathlib.Path('output/')
    faculty_list = list(p_temp.glob('*.csv'))
    # print(class_list)
    for faculty_csv_path in faculty_list:
        file_name = os.path.splitext(os.path.basename(faculty_csv_path))[0]
        with open('text/' + file_name + '.csv', 'w', encoding='utf-8') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(HEADER)
            print(file_name)
            with open(faculty_csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                i = 0
                for faculty_detail in reader:
                    if i==0:
                        i+=1
                        continue
                    print(faculty_detail)
                    name = remove(faculty_detail[0])
                    link = faculty_detail[1]
                    td_list = get_table_from_url(name, link)
                    if td_list==None:
                        continue
                    name = td_list[3]
                    grade = td_list[7]
                    class_no = td_list[9]
                    semester = td_list[13]
                    teacher = td_list[5]
                    detail_list = td_list[28:]
                    detail = ' '.join(map(str, detail_list))
                    row = [name, grade, class_no, semester, teacher, detail]
                    writer.writerow(row)
                

def remove(str):
    disturbers = ['\xa0', '\n', '\r', '\u3000', '<br>', '<br />', '</br>', '<br/>', '</>']
    for disturber in disturbers:
        str = str.replace(disturber, '')
    return str.strip()


if __name__ == "__main__":
    main()