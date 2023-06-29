import logging

import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm

from models.word2vec.src.preprocessor import TextPreProcessor

"""
Initializing a CBOW model which tries to guess the middle word in a
bag of words of size n. CBOW is a 2-layer neural net, layer 1 is
embeddings, layer 2 is a regression that predicts proabilities
via softmax
https://colab.research.google.com/gist/veekaybee/a40d8f37dd99eda2e6d03f4c10671674/cbow.ipynb

Example sentences: People create programs to direct processes.
Example Context: ['People','create','to', 'direct']
Example Prediction: 'programs'
"""


class CBOW(torch.nn.Module):
    def __init__(self):  # we pass in vocab_size and embedding_dim as hyperparams
        super(CBOW, self).__init__()
        self.num_epochs = 3
        self.context_size = 2  # 2 words to the left, 2 words to the right
        self.embedding_dim = 100  # Size of your embedding vector
        self.learning_rate = 0.001
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.vocab = TextPreProcessor().build_vocab()
        self.word_to_ix = self.vocab.get_stoi()
        self.ix_to_word = self.vocab.get_itos()
        self.vocab_list = list(self.vocab.get_stoi().keys())
        self.vocab_size = len(self.vocab)

        self.model = None

        self.model_path = "model.ckpt"

        # out: 1 x embedding_dim
        self.embeddings = nn.Embedding(
            self.vocab_size, self.embedding_dim
        )  # initialize an Embedding matrix based on our inputs
        self.linear1 = nn.Linear(self.embedding_dim, 128)
        self.activation_function1 = nn.ReLU()

        # out: 1 x vocab_size
        self.linear2 = nn.Linear(128, self.vocab_size)
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

    def build_training_data(self) -> list[tuple]:
        logging.warning("Building training data")

        vocab = self.vocab_list

        data = []
        for i in range(self.context_size, len(vocab) - self.context_size):
            context = [vocab[i - 2], vocab[i - 1], vocab[i + 1], vocab[i + 2]]
            target = vocab[i]
            data.append((context, target))

        return data

    def make_context_vector(self, context, word_to_ix) -> torch.LongTensor:
        """
        For each word in the vocab, find sliding windows of [-2,1,0,1,2] indexes
        relative to the position of the word

        :param vocab: list of words in the vocab
        :return: torch.LongTensor
        """
        idxs = [word_to_ix[w] for w in context]
        tensor = torch.LongTensor(idxs)

        return tensor

    def train_model(self):
        # Loss and optimizer
        self.model = CBOW().to(self.device)
        optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        loss_function = nn.NLLLoss()

        logging.warning("Building training data")
        data = self.build_training_data()

        logging.warning("Starting forward pass")
        for epoch in tqdm(range(self.num_epochs)):
            # we start tracking how accurate our intial words are
            total_loss = 0

            # for the x, y in the training data:
            for context, target in data:
                context_vector = self.make_context_vector(context, self.word_to_ix)

                # we look at loss
                log_probs = self.model(context_vector)

                total_loss += loss_function(log_probs, torch.tensor([self.word_to_ix[target]]))

            # optimize at the end of each epoch
            optimizer.zero_grad()
            total_loss.backward()
            optimizer.step()

            # Log out some metrics to see if loss decreases
            logging.warning("end of epoch {} | loss {:2.3f}".format(epoch, total_loss))

        torch.save(self.model.state_dict(), self.model_path)
        logging.warning(f"Save model to {self.model_path}")

    def load(self):
        """
        Load model from file
        :return:
        """
        try:
            logging.warning("Loading model from checkpoint")

            self.model = CBOW().to(self.device)
            self.model.eval()

            if torch.cuda.is_available():
                self.model.cpu()
                self.model.load_state_dict(torch.load(self.model_path))
                self.model = self.model.cuda()
            else:
                self.model.load_state_dict(torch.load(self.model_path))
            return self.model

        except FileNotFoundError:
            print("Model file does not exist")
