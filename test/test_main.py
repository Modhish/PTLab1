# -*- coding: utf-8 -*-
from src.main import get_path_from_arguments, get_reader
import src.main as main_module
import pytest


@pytest.fixture()
def correct_arguments_string() -> tuple[list[str], str]:
    return ["-p", "/home/user/file.txt"], "/home/user/file.txt"


@pytest.fixture()
def noncorrect_arguments_string() -> list[str]:
    return ["/home/user/file.txt"]


def test_get_path_from_correct_arguments(
        correct_arguments_string: tuple[list[str], str]) -> None:
    path = get_path_from_arguments(correct_arguments_string[0])
    assert path == correct_arguments_string[1]


def test_get_path_from_noncorrect_arguments(
        noncorrect_arguments_string: list[str]) -> None:
    with pytest.raises(SystemExit) as e:
        get_path_from_arguments(noncorrect_arguments_string[0])
    assert e.type == SystemExit


@pytest.mark.parametrize("path", ["data/data.json", "C:/DATA/FILE.JSON"])
def test_get_reader_for_json_file(path: str) -> None:
    # классы берутся из модуля main, чтобы сравнивать те же объекты классов
    assert isinstance(get_reader(path), main_module.JsonDataReader)


@pytest.mark.parametrize("path", ["data/data.txt", "data/file"])
def test_get_reader_for_text_file(path: str) -> None:
    assert isinstance(get_reader(path), main_module.TextDataReader)


@pytest.mark.parametrize("filename, content, expected", [
    ("data.json",
     '{"Иванов": {"химия": 95, "физика": 90}, "Петров": {"химия": 60}}',
     "Студент, имеющий 90 баллов минимум по 2 дисциплинам: Иванов"),
    ("data.txt",
     "Петров\n    химия:60\n    физика:91\n",
     "Студентов, имеющих 90 баллов минимум по 2 дисциплинам, нет"),
])
def test_main(tmpdir, monkeypatch, capsys, filename: str, content: str,
              expected: str) -> None:
    p = tmpdir.join(filename)
    p.write_text(content, encoding='utf-8')
    monkeypatch.setattr("sys.argv", ["main.py", "-p", str(p)])
    main_module.main()
    output = capsys.readouterr().out
    assert "Students: " in output
    assert "Rating: " in output
    assert expected in output
