from pathlib import Path
from typing import List

from optimum.onnxruntime import ORTModelForFeatureExtraction
from transformers import AutoTokenizer

from model.sentence_embedding_pipeline import SentenceEmbeddingPipeline


class ONNXEmbeddingGenerator:
    def __init__(self):
        # conf = config()
        # logging.config.fileConfig("/Users/vicki/viberary/logging.conf")
        self.onnx_path = Path("embedding_model")
        self.model = ORTModelForFeatureExtraction.from_pretrained(
            "sentence-transformers/msmarco-distilbert-base-v3", export=True
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            "sentence-transformers/msmarco-distilbert-base-v3"
        )
        self.ctx_pipeline = SentenceEmbeddingPipeline(model=self.model, tokenizer=self.tokenizer)

    def checkpoint_model(self):
        self.model.save_pretrained(self.onnx_path)
        self.tokenizer.save_pretrained(self.onnx_path)

    def generate_embeddings(self, inputs: List[str]):
        embeddings = self.ctx_pipeline(inputs)
        return embeddings
