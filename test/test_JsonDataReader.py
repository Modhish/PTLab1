# -*- coding: utf-8 -*-
import json

import pytest
from src.Types import DataType
from src.CalcRating import CalcRating
from src.JsonDataReader import JsonDataReader


class TestJsonDataReader:

    @pytest.fixture()
    def file_and_data_content(self) -> tuple[str, DataType]:
        text = json.dumps({
            "Иванов Иван Иванович": {
                "математика": 67,
                "литература": 100,
                "программирование": 91
            },
            "Петров Петр Петрович": {
                "математика": 78,
                "химия": 87,
                "социология": 61
            }
        }, ensure_ascii=False, indent=4)

        data: DataType = {
            "Иванов Иван Иванович": [
                ("математика", 67), ("литература", 100),
                ("программирование", 91)
            ],
            "Петров Петр Петрович": [
                ("математика", 78), ("химия", 87), ("социология", 61)
            ]
        }
        return text, data

    @pytest.fixture()
    def write_file(self, tmpdir):
        def _write(text: str) -> str:
            p = tmpdir.join("my_data.json")
            p.write_text(text, encoding='utf-8')
            return str(p)
        return _write

    def test_read(self, file_and_data_content: tuple[str, DataType],
                  write_file) -> None:
        path = write_file(file_and_data_content[0])
        assert JsonDataReader().read(path) == file_and_data_content[1]

    def test_read_keeps_subject_order(
            self, file_and_data_content: tuple[str, DataType],
            write_file) -> None:
        path = write_file(file_and_data_content[0])
        data = JsonDataReader().read(path)
        subjects = [s for s, _ in data["Иванов Иван Иванович"]]
        assert subjects == ["математика", "литература", "программирование"]

    def test_read_empty_object(self, write_file) -> None:
        assert JsonDataReader().read(write_file("{}")) == {}

    def test_read_student_without_subjects(self, write_file) -> None:
        data = JsonDataReader().read(
            write_file('{"Сидоров Олег Иванович": {}}'))
        assert data == {"Сидоров Олег Иванович": []}

    def test_read_boundary_scores(self, write_file) -> None:
        data = JsonDataReader().read(
            write_file('{"Сидоров": {"физика": 0, "химия": 100}}'))
        assert data == {"Сидоров": [("физика", 0), ("химия", 100)]}

    def test_read_invalid_json(self, write_file) -> None:
        with pytest.raises(json.JSONDecodeError):
            JsonDataReader().read(write_file('{"Иванов": {"химия": 90'))

    def test_read_root_is_not_object(self, write_file) -> None:
        with pytest.raises(ValueError, match="Корневой элемент"):
            JsonDataReader().read(write_file('[{"Иванов": {}}]'))

    def test_read_subjects_are_not_object(self, write_file) -> None:
        with pytest.raises(ValueError, match="должны быть объектом"):
            JsonDataReader().read(write_file('{"Иванов": [90, 80]}'))

    @pytest.mark.parametrize("score", ['"90"', "90.5", "true", "null"])
    def test_read_score_is_not_integer(self, write_file,
                                       score: str) -> None:
        with pytest.raises(ValueError, match="целым числом"):
            JsonDataReader().read(
                write_file('{"Иванов": {"химия": ' + score + '}}'))

    @pytest.mark.parametrize("score", [-1, 101])
    def test_read_score_out_of_range(self, write_file, score: int) -> None:
        with pytest.raises(ValueError, match="диапазоне"):
            JsonDataReader().read(
                write_file('{"Иванов": {"химия": ' + str(score) + '}}'))

    def test_read_missing_file(self, tmpdir) -> None:
        with pytest.raises(FileNotFoundError):
            JsonDataReader().read(str(tmpdir.join("missing.json")))

    def test_read_result_is_compatible_with_calc_rating(
            self, file_and_data_content: tuple[str, DataType],
            write_file) -> None:
        data = JsonDataReader().read(write_file(file_and_data_content[0]))
        rating = CalcRating(data).calc()
        assert rating["Иванов Иван Иванович"] == pytest.approx(86.0)
        assert rating["Петров Петр Петрович"] == pytest.approx(75.3333,
                                                               abs=0.001)
