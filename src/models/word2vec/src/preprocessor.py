from torchtext.vocab import Vocab, build_vocab_from_iterator

"""
Preprocess text from a CSV file that's created in the input_generator
into format for modeling CBOW or Skipgram
"""


class TextPreProcessor:
    def __init__(self) -> None:
        # TODO: create utility class for reading relative paths across the project
        self.input_file = "/Users/vicki/viberary/viberary/data/word2vec_input.csv"

        # TODO: split into training and test set

    def generate_tokens(self):
        with open(self.input_file, encoding="utf-8") as f:
            for line in f:
                line = line.replace("\\", "")  # Strip extra \\ in input text
                yield line.strip().split()

    def build_vocab(self) -> Vocab:
        vocab = build_vocab_from_iterator(self.generate_tokens(), specials=["<unk>"], min_freq=100)
        return vocab
