from collections import Counter
from pathlib import Path
import re
from typing import Union


TOKEN_PTRN = re.compile(r'\w+')


def tokenize(text: str) -> list[str]:
    return re.findall(TOKEN_PTRN, text)


class Ngrams:
    def __init__(self, data_folder: Union[Path, str]):
        self.data_folder = data_folder
        self.ngrams1: Counter[str, int] = Counter()
        self.ngrams2: Counter[str, int] = Counter()
        self.ngrams3: Counter[str, int] = Counter()

    def load_txt(self, file_name: Union[Path, str]) -> None:
        path = Path(self.data_folder) / file_name
        with open(path, 'r', encoding='utf-8') as source_file:
            text = source_file.read()
        text = text.lower()
        tokens = tokenize(text)
        self.ngrams1 = Counter(tokens)
        self.ngrams2 = Counter(' '.join(tokens[i:i + 2]) for i in range(len(tokens) - 1))
        self.ngrams3 = Counter(' '.join(tokens[i:i + 3]) for i in range(len(tokens) - 2))
