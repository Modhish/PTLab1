# -*- coding: utf-8 -*-
import pytest
from src.Types import DataType
from src.HighScoreStudentFinder import HighScoreStudentFinder


class TestHighScoreStudentFinder:

    @pytest.fixture()
    def input_data(self) -> DataType:
        return {
            "Иванов Иван Иванович": [
                ("математика", 67), ("литература", 100),
                ("программирование", 91)
            ],
            "Петров Петр Петрович": [
                ("математика", 78), ("химия", 87), ("социология", 61)
            ],
            "Сидорова Анна Сергеевна": [
                ("математика", 95), ("физика", 88),
                ("программирование", 90), ("английский язык", 72)
            ]
        }

    def test_init(self, input_data: DataType) -> None:
        finder = HighScoreStudentFinder(input_data)
        assert finder.data == input_data
        assert finder.min_score == 90
        assert finder.min_subjects == 2

    def test_count_high_scores(self, input_data: DataType) -> None:
        finder = HighScoreStudentFinder(input_data)
        assert finder.count_high_scores("Иванов Иван Иванович") == 2
        assert finder.count_high_scores("Петров Петр Петрович") == 0
        assert finder.count_high_scores("Сидорова Анна Сергеевна") == 2

    def test_find_returns_qualifying_student(self,
                                             input_data: DataType) -> None:
        student = HighScoreStudentFinder(input_data).find()
        assert student in ("Иванов Иван Иванович",
                           "Сидорова Анна Сергеевна")

    def test_find_score_exactly_90_counts(self) -> None:
        data: DataType = {"Козлов": [("химия", 90), ("физика", 90)]}
        assert HighScoreStudentFinder(data).find() == "Козлов"

    def test_find_score_89_does_not_count(self) -> None:
        data: DataType = {"Козлов": [("химия", 90), ("физика", 89)]}
        assert HighScoreStudentFinder(data).find() is None

    def test_find_one_high_subject_is_not_enough(self) -> None:
        data: DataType = {"Козлов": [("химия", 100), ("физика", 60),
                                     ("биология", 75)]}
        assert HighScoreStudentFinder(data).find() is None

    def test_find_skips_students_who_do_not_qualify(self) -> None:
        data: DataType = {
            "Первый": [("химия", 95)],
            "Второй": [("химия", 95), ("физика", 92)]
        }
        assert HighScoreStudentFinder(data).find() == "Второй"

    def test_find_in_empty_data(self) -> None:
        assert HighScoreStudentFinder({}).find() is None

    def test_find_student_without_subjects(self) -> None:
        assert HighScoreStudentFinder({"Пустой": []}).find() is None

    @pytest.mark.parametrize("min_score, min_subjects, expected", [
        (100, 1, "Иванов Иван Иванович"),
        (95, 1, "Иванов Иван Иванович"),
        (90, 3, None),
        (60, 3, "Иванов Иван Иванович"),
        (88, 3, "Сидорова Анна Сергеевна"),
    ])
    def test_find_with_custom_thresholds(self, input_data: DataType,
                                         min_score: int, min_subjects: int,
                                         expected: str | None) -> None:
        finder = HighScoreStudentFinder(input_data, min_score, min_subjects)
        assert finder.find() == expected

    def test_get_message_when_found(self) -> None:
        data: DataType = {"Козлов": [("химия", 90), ("физика", 99)]}
        message = HighScoreStudentFinder(data).get_message()
        assert message == ("Студент, имеющий 90 баллов минимум "
                           "по 2 дисциплинам: Козлов")

    def test_get_message_when_not_found(self) -> None:
        data: DataType = {"Козлов": [("химия", 50)]}
        message = HighScoreStudentFinder(data).get_message()
        assert message == ("Студентов, имеющих 90 баллов минимум "
                           "по 2 дисциплинам, нет")
