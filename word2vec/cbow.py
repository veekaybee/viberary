from torch.utils.data import Dataset
from torchvision import datasets
from torchtext.vocab import vocab

import csv
from collections import Counter

# TODO: abstract away util from local file dir
input_file = "/Users/vicki/viberary/viberary/data/word2vec_input.csv"

# Open file
def read_input_data(input_file) -> list:

    rows = []

    with open(input_file, "rt") as input_file:
        for row in csv.reader(input_file):
            rows.append(row)

    # Build vocabulary from file


def create_vocabulary_counter(input_data: list[str]) -> Counter:

    counter = Counter()

    for item in input_data:
        counter.update(item)

    return counter


def build_vocab(
    vocab_counter: Counter, tokens=list[str]
) -> torchtext.vocab.vocab.Vocab:

    vocab = text.build_vocab_from_iterator(vocab_counter)
    return vocab
