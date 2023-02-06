from word2vec.preprocessor import TextPreProcessor
import torch.nn as nn

# TODO: tune these based on intiuition
EMBED_DIMENSION = 64
EMBED_MAX_NORM = 1

"""
We implement training each book sample as an individual paragraph
"""


class CBOWModel(nn.Module):
    def __init__(self, vocab_size, ebd_size, cont_size):
        super(CBOWModel, self).__init__()

        self.ebd = nn.Embedding(vocab_size, ebd_size)
        self.lr1 = nn.Linear(ebd_size * cont_size * 2, 128)
        self.lr2 = nn.Linear(128, vocab_size)

        self._init_weight()

    def forward(self, inputs):
        out = self.ebd(inputs).view(1, -1)
        out = nn.functional.relu(self.lr1(out))
        out = self.lr2(out)
        out = nn.functional.log_softmax(out)
        return out

    def _init_weight(self, scope=0.1):
        self.ebd.weight.data.uniform_(-scope, scope)
        self.lr1.weight.data.uniform_(0, scope)
        self.lr1.bias.data.fill_(0)
        self.lr2.weight.data.uniform_(0, scope)
        self.lr2.bias.data.fill_(0)
