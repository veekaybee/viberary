import torch
from train import ModelTrainer


## instantiate CBOW, generating training data
mt = ModelTrainer()
model = mt.train_model()


## TESTING
context = ['third', 'shapeshifter', '2016', 'for']
context_vector = mt.make_context_vector(context, mt.word_to_ix)
a = model(context_vector)

# Return results
print(f'Raw text: {mt.vocab}')
print(f"Context: {context}\n")
print(f"Prediction: {mt.ix_to_word[torch.argmax(a[0]).item()]}")
