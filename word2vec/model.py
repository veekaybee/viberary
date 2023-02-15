from word2vec.preprocessor import TextPreProcessor
import torch
import torch.nn as nn


"""
Initializing a CBOW model which tries to guess the middle word in a
bag of words of size n. CBOW is a 2-layer neural net, layer 1 is 
embeddings, layer 2 is a regression that predicts proabilities
via softmax
See more here: https://colab.research.google.com/gist/veekaybee/a40d8f37dd99eda2e6d03f4c10671674/cbow.ipynb

Example sentences: People create programs to direct processes.
Example Context: ['People','create','to', 'direct']
Example Prediction: 'programs'
"""

class CBOW(torch.nn.Module):
    def __init__(self, vocab_size, embedding_dim): # we pass in vocab_size and embedding_dim as hyperparams
        super(CBOW, self).__init__()

        # out: 1 x embedding_dim
        self.embeddings = nn.Embedding(vocab_size, embedding_dim) # initialize an Embedding matrix based on our inputs
        self.linear1 = nn.Linear(embedding_dim, 128)
        self.activation_function1 = nn.ReLU()

        # out: 1 x vocab_size
        self.linear2 = nn.Linear(128, vocab_size)
        self.activation_function2 = nn.LogSoftmax(dim=-1)

    def forward(self, inputs):
        embeds = sum(self.embeddings(inputs)).view(1, -1)
        out = self.linear1(embeds)
        out = self.activation_function1(out)
        out = self.linear2(out)
        out = self.activation_function2(out)
        return out

    def get_word_embedding(self, word, word_to_ix):
        word = torch.tensor([word_to_ix[word]])
        # Embeddings lookup of a single word once the Embeddings layer has been optimized 
        return self.embeddings(word).view(1, -1)
