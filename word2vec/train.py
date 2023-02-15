from word2vec.model import CBOW
from word2vec.preprocessor import TextPreProcessor

import logging
import torch
import torch.nn as nn
import torch.optim as optim

from tqdm import tqdm


class ModelTrainer:
    def __init__(self) -> None:

        # Hyperparameters
        self.num_epochs = 50
        self.context_size = 2  # 2 words to the left, 2 words to the right
        self.embedding_dim = 100  # Optimized for storage
        self.learning_rate = 0.001
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.vocab = TextPreProcessor().build_vocab()
        self.word_to_ix = self.vocab.get_stoi()
        self.ix_to_word = self.vocab.get_itos()
        self.vocab_list = list(self.vocab.get_stoi().keys())
        self.vocab_size = len(self.vocab)

    def build_training_data(self) -> list[tuple]:

        logging.warning('Building training data')

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

    def train_model(self) -> CBOW:
        # Main model training loop

        # Loss and optimizer
        model = CBOW(self.vocab_size, self.embedding_dim).to(self.device)
        optimizer = optim.Adam(model.parameters(), lr=self.learning_rate)
        loss_function = nn.NLLLoss()

        logging.warning('Building training data')
        data = self.build_training_data()

        logging.warning('Starting forward pass')
        for epoch in tqdm(range(self.num_epochs)):
            # we start tracking how accurate our intial words are
            total_loss = 0

            # for the x, y in the training data:
            for context, target in data:
                context_vector = self.make_context_vector(context, self.word_to_ix)

                # we look at loss
                log_probs = model(context_vector)

                # we compare the loss from what the actual word is related to the probaility of the words
                total_loss += loss_function(
                    log_probs, torch.tensor([self.word_to_ix[target]])
                )

            # optimize at the end of each epoch
            optimizer.zero_grad()
            total_loss.backward()
            optimizer.step()

            # Log out some metrics to see if loss decreases
            logging.warning("end of epoch {} | loss {:2.3f}".format(epoch, total_loss))

        torch.save(model.state_dict(), 'model.ckpt')
        logging.warning('Save model to model.ckpt')

        return model
