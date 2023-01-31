from train import ModelTrainer
from model import EMBED_DIMENSION

model = ModelTrainer(300,EMBED_DIMENSION)

#TESTING
context = ['People','create','to', 'direct']
context_vector = model.make_context_vector(context, word_to_ix)
a = model(context_vector)

#Print result
print(f'Raw text: {" ".join(raw_text)}\n')
print(f'Context: {context}\n')
print(f'Prediction: {ix_to_word[torch.argmax(a[0]).item()]}')