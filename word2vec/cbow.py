import csv
import sys
from collections import Counter

import torchtext
from torch.utils.data import Dataset
from torchtext.vocab import build_vocab_from_iterator
from torchvision import datasets

"""
This class implements the CBOW approach to learning embeddings covered in the original Word2vec paper. 
"""


class ContinuousBagofWords:
    def __init__(self) -> None:

        # TODO: create utility class for reading relative paths across the project
        self.input_file = "/Users/vicki/viberary/viberary/data/word2vec_input.csv"

    # Open file
    def read_input_data(self, input_file) -> list:
        """Reads a comma-delimited CSV file of rows of book data

        Args:
            input_file (_type_): CSV-delimited file

        Returns:
            list: A concatentated in-memory list representation of all books in our training data
        """

        rows = []
        self.input_file = input_file

        csv.field_size_limit(sys.maxsize)

        with open(input_file, "rt") as input_file:
            for row in csv.reader(input_file, quoting=csv.QUOTE_NONE):
                rows.append(row)
        
        return rows

    def create_vocabulary_counter(self, input_data: list[str]) -> Counter:

        counter = Counter()
        
        for item in input_data:
            counter.update(item)

        return counter

    def build_vocab(self):

        input_data = self.read_input_data(self.input_file)
        vocabulary_counter = self.create_vocabulary_counter(input_data)
        print(vocabulary_counter)
        # vocab = build_vocab_from_iterator(vocabulary_counter)
        # return vocab


vocab = ContinuousBagofWords().build_vocab()

print(vocab)
