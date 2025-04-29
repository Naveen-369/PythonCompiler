import pytest
from file_reader import *


def test_file_reader_reads_content(tmp_path):
    # Create a temporary file
    file = tmp_path / "main.py"
    file.write_text("a = 5")
    reader = file_reader(str(file))
    print(reader.lines)
    assert reader.lines == ['a = 5']


def test_file_reader_missing_file():
    with pytest.raises(FileNotFoundError):
        reader = file_reader("non_existent.txt")
