import csv
from typing import *


def is_diphthong(phoneme: str):
    if len(phoneme) > 2:
        raise Exception("Malformed Phoneme")
    if len(phoneme) == 2 and phoneme[1] != "ː":
        return True
    return False


def extract_acoustics(row: dict, acoustics: str, extract_func: Callable):
    """
    :param row: a row in csv
    :param acoustics: could be one of f0, F1, F2, or F3
    :param extract_func: a usr defined function to extract feature, say, movement
    :return:
    """
    if acoustics not in ("f0", "F1", "F2", "F3"):
        raise Exception("Invalid acoustics type")
    header_names = [acoustics + i for i in ["A", "B", "C"]]
    values = [float(row[header_name]) for header_name in header_names]  # e.g. three values for f0
    return extract_func(values)


def read_data():
    with open('LING401_milestone3_cantonese/Vowels.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for line_cnt, row in enumerate(csv_reader):
            if line_cnt == 0:  # header
                print("Headers: ", ",".join(row))
            else:
                yield row


if __name__ == "__main__":
    for row in read_data():
        print(row["Phone"])
        extract_acoustics(row, "f0", print)
