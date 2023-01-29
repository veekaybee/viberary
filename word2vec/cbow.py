from word2vec.preprocessor import TextPreProcessor

import torch.nn as nn 

#TODO: tune these based on intiuition
EMBED_DIMENSION = 300 
EMBED_MAX_NORM = 1 

'''
We implement training each book sample as an individual paragraph
'''
class CBOW_Model(nn.Module):
    def __init__(self, vocab_size: int):
        super(CBOW_Model, self).__init__()
        self.embeddings = nn.Embedding(
            num_embeddings=vocab_size,
            embedding_dim=EMBED_DIMENSION,
            max_norm=EMBED_MAX_NORM,
        )
        
        # Linear transformation to the size of the model based on sampled input
        self.linear = nn.Linear(
            in_features=EMBED_DIMENSION,
            out_features=vocab_size,
        )
    

    def forward(self, inputs_):
        x = self.embeddings(inputs_)
        x = x.mean(axis=1)
        x = self.linear(x)
        return x