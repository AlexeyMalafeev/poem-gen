from collections import Counter
from pathlib import Path
import random
import re
from typing import Union


TOKEN_PTRN = re.compile(r'\w+')


def tokenize(text: str) -> list[str]:
    return re.findall(TOKEN_PTRN, text)


class NaiveNgrams:
    def __init__(self, data_folder: Union[Path, str], randomness: float = 0.1):
        self.data_folder = data_folder
        self.randomness = randomness
        self.ngrams1: Counter[str, int] = Counter()
        self.ngrams2: Counter[str, int] = Counter()
        self.ngrams3: Counter[str, int] = Counter()

    def generate(self, prompt: str, max_len: int = 30) -> str:
        result: list[str] = tokenize(prompt)
        for _ in range(max_len):
            next_word = self.next_word(' '.join(result[-2:]))
            result.append(next_word)
        return ' '.join(result)

    def load_txt(self, file_name: Union[Path, str]) -> None:
        path = Path(self.data_folder) / file_name
        with open(path, 'r', encoding='utf-8') as source_file:
            text = source_file.read()
        text = text.lower()
        tokens = tokenize(text)
        self.ngrams1 = Counter(tokens)
        self.ngrams2 = Counter(' '.join(tokens[i:i + 2]) for i in range(len(tokens) - 1))
        self.ngrams3 = Counter(' '.join(tokens[i:i + 3]) for i in range(len(tokens) - 2))

    def next_word(self, prompt: str) -> str:
        prompt = prompt.strip()
        if not prompt or random.random() <= self.randomness:
            return random.choice(list(self.ngrams1))
        pool = []
        if ' ' in prompt:
            pool = [
                ngram.split()[-1]
                for ngram in self.ngrams3
                if ngram.startswith(f'{prompt} ')
            ]
        if not pool:
            pool = [
                ngram.split()[-1]
                for ngram in self.ngrams2
                if ngram.startswith(f'{prompt} ')
            ]
        if not pool:
            pool = list(self.ngrams1)
        return random.choice(pool)
