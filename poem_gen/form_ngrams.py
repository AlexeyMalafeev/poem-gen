from collections import Counter
from functools import cache
from pathlib import Path
import random
import re
from typing import Union


YEAR_PTRN = re.compile(r'\d{4}')
LINE_BREAK = 'BR'
TOKEN_PTRN = re.compile(r'\w+')


def tokenize(text: str) -> list[str]:
    return re.findall(TOKEN_PTRN, text)


class FormNgrams:
    def __init__(self, data_folder: Union[Path, str], randomness: float = 0.0):
        self.data_folder = data_folder
        self.randomness = randomness
        self.ngrams1: Counter[str, int] = Counter()
        self.ngrams2: Counter[str, int] = Counter()
        self.ngrams3: Counter[str, int] = Counter()
        self.ngrams_for_sampling: list[str] = []

    def generate(self, prompt: str, max_len: int = 30) -> str:
        result: list[str] = tokenize(prompt)
        for _ in range(max_len):
            next_word = self.next_word(' '.join(result[-2:]))
            result.append(next_word)
        text = ' '.join(result)
        return re.sub(rf' ?{LINE_BREAK} ?', '\n', text)

    @cache
    def _get_candidates(self, prompt):
        ngrams = self.ngrams3 if ' ' in prompt else self.ngrams2
        return [
            ngram.split()[-1]
            for ngram, freq in ngrams.items()
            if ngram.startswith(f'{prompt} ')
            for _ in range(freq)
        ]

    def load_txt(self, file_name: Union[Path, str]) -> None:
        path = Path(self.data_folder) / file_name
        tokens = []
        with open(path, 'r', encoding='utf-8') as source_file:
            for line in source_file:
                if (line := line.strip()) and not re.fullmatch(YEAR_PTRN, line):
                    tokens.extend(tokenize(f'{line.lower()} {LINE_BREAK}'))
        self.ngrams1 = Counter(tokens)
        self.ngrams2 = Counter(' '.join(tokens[i:i + 2]) for i in range(len(tokens) - 1))
        self.ngrams3 = Counter(' '.join(tokens[i:i + 3]) for i in range(len(tokens) - 2))
        self.ngrams_for_sampling = [unigram for unigram, freq in self.ngrams1.items() for _ in range(freq)]

    def _next_from_1grams(self) -> str:
        return random.choice(self.ngrams_for_sampling)

    def _next_from_2_3_grams(self, prompt: str) -> str:
        pool = self._get_candidates(prompt)
        return random.choice(pool) if pool else ''

    def next_word(self, prompt: str) -> str:
        prompt = prompt.strip()
        if not prompt or random.random() <= self.randomness:
            return self._next_from_1grams()
        next_word = self._next_from_2_3_grams(prompt)
        return next_word or self._next_from_1grams()
