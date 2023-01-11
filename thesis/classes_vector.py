import csv
import os
import pathlib

from collections import Counter

import numpy as np
import tfidf_nn
import tfidf_nn1
import classes_mecab


def get_filename_list():
    file_path = pathlib.Path('thesis/faculty/初等教育教員養成課程国語選修　日本語教育コース/')
    filename_list = list(file_path.glob('*.txt'))
    return filename_list


def get_namefaculty_from_path(filename_path):
    filename_path = str(filename_path)
    target1 = 'thesis/faculty/'
    idx1 = filename_path.find(target1)
    target2 = '.txt'
    idx2 = filename_path.find(target2)
    filename_plane = filename_path[idx1+len(target1):idx2]
    # print(filename)

    sep = '/'
    name = filename_plane.split(sep)

    faculty = name[0]
    planename = name[1]

    return faculty, planename


def create_faculty_directory(faculty_name):
    os.makedirs('thesis/faculty_tfidf/' + faculty_name, exist_ok=True)
    # os.makedirs('thesis/faculty_csv/' + faculty_name, exist_ok=True)


def main():
    filename_list = get_filename_list()
    file_tfidf_dict = {}
    file_tfidf_dict = tfidf_nn1.create_tfidf_dict(filename_list)
    file_vector_dict = {}
    for filename in filename_list:
        file_tfidf = file_tfidf_dict[filename]
        print(file_tfidf)
        try:
            tfidf_nn1.print_tfidf_dict(file_tfidf, filename)
        except:
            pass

    for filename in filename_list:
        tfidf_sorted = sorted(file_tfidf_dict[filename].items(), key=lambda x:x[1], reverse=True)
        # tfidf_sorted_list = np.array(tfidf_sorted)
        tfidf_sorted_wordlist = list(map(lambda x:x[0], tfidf_sorted))
        # print(tfidf_sorted_wordlist)
        top_word = tfidf_sorted_wordlist[:700]
        # print(len(top_word))
        # 特徴語リスト上位700 = top_word（リスト）

        faculty, planename = get_namefaculty_from_path(filename)
        create_faculty_directory(faculty)
        path = "thesis/faculty_tfidf/" + faculty

        with open(path + '/' + planename + '.txt', 'w', encoding='utf-8') as output_file:
            for x in tfidf_sorted:
                output_file.write(str(x) + "\n")
            output_file.close()

        file_vector_dict[filename] = tfidf_nn1.text_vector(top_word)

    HEADER = ['name', 'faculty', 'vector']

    faculty_list = classes_mecab.get_faculty_list()
    for faculty_file in faculty_list:
        faculty_name = classes_mecab.get_name_from_path(faculty_file)
        print(faculty_list)
        print(faculty_file)
        print(faculty_name)
        for filename in filename_list:
            faculty, planename = get_namefaculty_from_path(filename)

            with open('thesis/faculty_csv/' + faculty_name + '.csv', 'w', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(HEADER)
                if faculty_name == faculty:
                    break
                else:
                    print('faculty:{0}'.format(faculty))
                    print('name:{0}'.format(planename))
                    vector = file_vector_dict[filename]
                    print('vector:{0}'.format(vector))
                    print()
                    row =[planename, faculty, vector]
                    writer.writerow(row)


if __name__ == "__main__":
    main()