# -*- coding: utf-8 -*-
from Types import DataType


class HighScoreStudentFinder:
    """Поиск студента, имеющего не менее min_score баллов
    минимум по min_subjects дисциплинам (вариант 12)."""

    def __init__(self, data: DataType, min_score: int = 90,
                 min_subjects: int = 2) -> None:
        self.data: DataType = data
        self.min_score: int = min_score
        self.min_subjects: int = min_subjects

    def count_high_scores(self, student: str) -> int:
        return sum(1 for _, score in self.data[student]
                   if score >= self.min_score)

    def find(self) -> str | None:
        for student in self.data:
            if self.count_high_scores(student) >= self.min_subjects:
                return student
        return None

    def get_message(self) -> str:
        student = self.find()
        if student is None:
            return (f"Студентов, имеющих {self.min_score} баллов минимум "
                    f"по {self.min_subjects} дисциплинам, нет")
        return (f"Студент, имеющий {self.min_score} баллов минимум "
                f"по {self.min_subjects} дисциплинам: {student}")
