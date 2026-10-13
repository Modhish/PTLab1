# -*- coding: utf-8 -*-
import json

from Types import DataType
from DataReader import DataReader


class JsonDataReader(DataReader):
    """Чтение данных о студентах из файла формата JSON.

    Ожидаемая структура файла:
    {
        "Иванов Иван Иванович": {"математика": 67, "литература": 100},
        "Петров Петр Петрович": {"химия": 87}
    }
    """

    MIN_SCORE: int = 0
    MAX_SCORE: int = 100

    def __init__(self) -> None:
        self.students: DataType = {}

    def read(self, path: str) -> DataType:
        with open(path, encoding='utf-8') as file:
            content = json.load(file)

        if not isinstance(content, dict):
            raise ValueError("Корневой элемент JSON должен быть объектом")

        for student, subjects in content.items():
            if not isinstance(subjects, dict):
                raise ValueError(
                    f"Оценки студента '{student}' должны быть объектом")
            self.students[student] = [
                (subject, self._check_score(student, subject, score))
                for subject, score in subjects.items()
            ]
        return self.students

    def _check_score(self, student: str, subject: str, score) -> int:
        # bool является подклассом int, поэтому исключается явно
        if isinstance(score, bool) or not isinstance(score, int):
            raise ValueError(
                f"Балл '{student}' по предмету '{subject}' "
                f"должен быть целым числом")
        if not self.MIN_SCORE <= score <= self.MAX_SCORE:
            raise ValueError(
                f"Балл '{student}' по предмету '{subject}' "
                f"должен быть в диапазоне "
                f"[{self.MIN_SCORE}; {self.MAX_SCORE}]")
        return score
