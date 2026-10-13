# -*- coding: utf-8 -*-
import argparse
import sys

from CalcRating import CalcRating
from DataReader import DataReader
from HighScoreStudentFinder import HighScoreStudentFinder
from JsonDataReader import JsonDataReader
from TextDataReader import TextDataReader


def get_path_from_arguments(args) -> str:
    parser = argparse.ArgumentParser(description="Path to datafile")
    parser.add_argument("-p", dest="path", type=str, required=True,
                        help="Path to datafile")
    args = parser.parse_args(args)
    return args.path


def get_reader(path: str) -> DataReader:
    if path.lower().endswith(".json"):
        return JsonDataReader()
    return TextDataReader()


def main():
    path = get_path_from_arguments(sys.argv[1:])

    reader = get_reader(path)
    students = reader.read(path)
    print("Students: ", students)

    rating = CalcRating(students).calc()
    print("Rating: ", rating)

    print(HighScoreStudentFinder(students).get_message())


if __name__ == "__main__":
    main()
