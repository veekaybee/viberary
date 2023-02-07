from word2vec.preprocessor import TextPreProcessor
import torch.nn as nn


"""
Initializing a CBOW model which tries to guess the middle word in a
bag of words of size n. CBOW is a 2-layer neural net

Example sentences: People create programs to direct processes.
Example Context: ['People','create','to', 'direct']
Example Prediction: 'programs'
"""


class CBOWModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim):
        super(CBOWModel, self).__init__()

        # Initialize three layers, one that reads in
        # applies a linear transformation to the incoming data:

        # The input to the module is a list of indices, and the output is the corresponding word embeddings.
        # Input is the size of the vocab dictionary and the size of each vector
        # We include two linear layers and one softmax
        self.embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.linear1 = nn.Linear(embedding_dim, 128)
        self.activation_function1 = nn.ReLU()

        # Softmax is the probability of the output word being correct
        self.linear2 = nn.Linear(128, vocab_size)
        self.activation_function2 = nn.LogSoftmax(dim=-1)

    # The forward pass returns the probability for each word in the vocabulary
    def forward(self, inputs):
        embeds = sum(self.embeddings(inputs)).view(1, -1)
        out = self.linear1(embeds)
        out = self.activation_function1(out)
        out = self.linear2(out)
        out = self.activation_function2(out)
        return out
