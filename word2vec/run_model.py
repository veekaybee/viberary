import torch
from word2vec.train import ModelTrainer
from word2vec.model import EMBED_DIMENSION

model = ModelTrainer(300, EMBED_DIMENSION)

# Epochs/loss
# print(model.train_model())


## TESTING
context = ['third', 'shapeshifter', '2016', 'for']
context_vector = model.make_context_vector(context)
print(context_vector)
a = model(context_vector)

# Print result
print(f'Raw text: {" ".join(model.vocab)}\n')
print(f'Context: {context}\n')
print(f'Prediction: {model.ix_to_word[torch.argmax(a[0]).item()]}')
