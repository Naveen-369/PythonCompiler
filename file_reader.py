import sys
from typing import List


class FileObject:
    def __init__(self, lines: List[str] = None):
        self.lines = lines
        self.current_line = 0
        self.line_num = 0
        self.col_num = 0

    def at(self, lineNo):
        return self.lines[lineNo]

    def __len__(self):
        return len(self.lines)

    def current_char(self):
        return self.lines[self.line_num][self.col_num]

    def advance(self):
        pass


# move col, wrap to next line, etc

def file_reader(inp: str) -> FileObject:
    """
    reads the inp file and return the list of list about the contents / text of the file
    :param inp: filename
    :return: FileObject with List of strings, each representing a line
    """
    text = []
    with open(inp, "r") as f:
        for line in f:
            text.append(line.rstrip('\n'))
    fileObj = FileObject(text)
    return fileObj
