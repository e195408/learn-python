import csv
import os
import pathlib
import unicodedata

import mecab_nn


def get_faculty_list():
    p_temp = pathlib.Path('text/')
    faculty_list = list(p_temp.glob('*.csv'))
    return faculty_list


def create_faculty_directory(faculty_name):
    os.makedirs('thesis/faculty/' + faculty_name, exist_ok=True)


def get_name_from_path(faculty_file):
    faculty_file = str(faculty_file)
    target1 = 'text/'
    idx1 = faculty_file.find(target1)
    target2 = '.csv'
    idx2 = faculty_file.find(target2)
    faculty_name = faculty_file[idx1+len(target1):idx2]
    print(faculty_name)

    return faculty_name


def morphological(faculty_file, faculty_name):
    with open(faculty_file, mode='r', encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        # header = next(input_file)
        print(faculty_file)

        for row in reader:
            # print(row)
            raw = row[5]
            text = mecab_nn.strip_CRLF_from_Text(raw)
            text = unicodedata.normalize('NFC', text)
            print(row[0])
            name = row[0].replace('/', ' ')

            path = "thesis/faculty/" + faculty_name

            with open(path + '/' + name + '_' + row[4] + '.txt', 'w') as txtf:
                txtf.write(mecab_nn.my_mecab(text))
                txtf.close()


def main():
    faculty_list = get_faculty_list()
    for faculty_file in faculty_list:
        faculty_name = get_name_from_path(faculty_file)
        create_faculty_directory(faculty_name)

        morphological(faculty_file, faculty_name)


if __name__ == "__main__":
    main()


