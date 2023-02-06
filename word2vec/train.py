from word2vec.model import CBOWModel
from word2vec.preprocessor import TextPreProcessor

import logging
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.autograd as autograd


class ModelTrainer:
    def __init__(self, vocab_size: int, embedding_dim: int) -> None:

        # Build vocab from input file, returns vocab object
        self.vocab = TextPreProcessor().build_vocab()
        self.word_to_ix = self.vocab.get_stoi()
        self.ix_to_word = self.vocab.get_itos()
        self.vocab_list = list(self.vocab.get_stoi().keys())
        self.vocab_size = len(self.vocab)

        # Hyperparameters
        self.num_epochs = 5
        self.context_size = 2  # 2 words to the left, 2 to the right
        self.embedding_dim = 64
        self.learning_rate = 0.001
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def get_context_window(self, vocab: list[str]) -> list[tuple]:
        """
        For each word in the vocab, find sliding windows of [-2,1,0,1,2] indexes
        relative to the position of the word

        :param vocab: list of words in the vocab
        :return: a list of tuples that are context windows for each word
        """

        self.vocab_list = vocab

        data = []
        for i in range(2, len(vocab) - 2):
            context = [vocab[i - 2], vocab[i - 1], vocab[i + 1], vocab[i + 2]]
            target = vocab[i]
            data.append((context, target))

        return data

    def make_context_vector(self, context) -> autograd.Variable:
        """

        :param context:
        :return:
        """
        idxs = [self.word_to_ix[w] for w in context]
        tensor = torch.LongTensor(idxs)

        return autograd.Variable(tensor)

    def train_model(self):
        # Main model training loop

        # Loss and optimizer
        self.model = CBOWModel(
            self.vocab_size, self.embedding_dim, self.context_size
        ).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)

        for epoch in range(self.num_epochs):
            total_loss = 0.0

            # generate context window for all words
            data = self.get_context_window(self.vocab_list)

            # for each word, context pair, crate a complementary vector and set the target vector
            for context, target in data:
                print(context, target)
                v_ctx = self.make_context_vector(context)
                v_tar = autograd.Variable(torch.LongTensor([self.vocab[target]]))

                # Forward pass
                self.model.zero_grad()
                out = self.model(v_ctx)

                # negative log likelihood loss, predicts the likelhood of the next word
                loss_function = nn.NLLLoss()
                loss = loss_function(out, v_tar)
                total_loss += loss.data

                # Backward pass and optimize
                loss.backward()

                # continue
                self.optimizer.step()

            logging.warning('Save model to model.ckpt')
            print("Save model to model.ckpt".format(epoch, total_loss))
            torch.save(self.model.state_dict(), 'model.ckpt')
            print("end of epoch {} | loss {:2.3f}".format(epoch, total_loss))
