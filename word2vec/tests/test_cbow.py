from word2vec.src.preprocessor import TextPreProcessor


def test_inputs():
    processor = TextPreProcessor()
    assert processor.build_vocab() is not None


def test_embeddings_outputs():
    pass
