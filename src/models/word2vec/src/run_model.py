import tensorboard as tb
import tensorflow as tf
import torch
from model import CBOW
from torch.utils.tensorboard import SummaryWriter

tf.io.gfile = tb.compat.tensorflow_stub.io.gfile

# instantiate CBOW, generating training data
cbow = CBOW()
# instantiate tensorboard
writer = SummaryWriter("/tmp/log")

# Train new model and checkpoint it
# cbow.train_model()

## Load trained model
model = cbow.load()

# Test word prediction
context = ["third", "shapeshifter", "2016", "for"]
context_vector = model.make_context_vector(context, model.word_to_ix)
a = model(context_vector)

# Return results
print(f"Raw text: {model.vocab}")
print(f"Context: {context}\n")
print(f"Prediction: {model.ix_to_word[torch.argmax(a[0]).item()]}")

# Check Embeddings Final Weights
print("Getting weights:\n", model.embeddings.weight.data[1])

# Check Embeddings
print("Getting embeddings:\n", model.embeddings)

vectors = model.embeddings.weight

# Write embeddings to file
writer.add_embedding(vectors)
writer.flush()
writer.close()
