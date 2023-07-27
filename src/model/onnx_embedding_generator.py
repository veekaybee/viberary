from pathlib import Path
from typing import List

from optimum.onnxruntime import ORTModelForFeatureExtraction
from transformers import AutoTokenizer

from model.sentence_embedding_pipeline import SentenceEmbeddingPipeline


class ONNXEmbeddingGenerator:
    def __init__(self, conf_manager):
        self.conf = conf_manager.get_config_file()
        self.onnx_path = self.conf["model"]["onnx_path"]
        self.root_path = conf_manager.get_root_dir()
        self.onnx_path = Path(f"{self.root_path}/{self.onnx_path}")
        self.model = ORTModelForFeatureExtraction.from_pretrained(self.onnx_path)
        self.tokenizer = AutoTokenizer.from_pretrained(self.onnx_path)
        self.pipeline = SentenceEmbeddingPipeline(model=self.model, tokenizer=self.tokenizer)

    def generate_embeddings(self, inputs: List[str]):
        embeddings = self.pipeline(inputs)
        return embeddings
