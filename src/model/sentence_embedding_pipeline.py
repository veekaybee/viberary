import torch
import torch.nn.functional as F
from transformers import Pipeline

from model.onnx_converter import ONNXConverter


class SentenceEmbeddingPipeline(Pipeline):
    def __init__(self):
        self.onnx = ONNXConverter()
        self.model = self.onnx.onnx_model_path
        self.tokenizer = self.onnx.onnx_model_path

    def mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[
            0
        ]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
            input_mask_expanded.sum(1), min=1e-9
        )

    def _sanitize_parameters(self, **kwargs):
        # we don't have any hyperameters to sanitize
        preprocess_kwargs = {}
        return preprocess_kwargs, {}, {}

    def preprocess(self, inputs):
        encoded_inputs = self.tokenizer(inputs, padding=True, truncation=True, return_tensors="pt")
        return encoded_inputs

    def _forward(self, model_inputs):
        outputs = self.model(**model_inputs)
        return {"outputs": outputs, "attention_mask": model_inputs["attention_mask"]}

    def postprocess(self, model_outputs):
        # Perform pooling
        sentence_embeddings = self.mean_pooling(
            model_outputs["outputs"], model_outputs["attention_mask"]
        )
        # Normalize embeddings
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
        return sentence_embeddings
