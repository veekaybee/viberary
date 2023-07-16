import logging
import logging.config
from pathlib import Path

from optimum.onnxruntime import ORTModelForFeatureExtraction
from transformers import AutoTokenizer

from inout.file_reader import get_config_file as config


class ONNXConverter:
    """
    Converts the Sentence Transformer Model to ONNX for Inference
    """

    def __init__(self):
        conf = config()
        logging.config.fileConfig(Path(conf["logging"]["path"]))
        self.model = conf["model"]["name"]
        self.onnx_model_path = Path(conf["model"]["onnx_path"])

    def convert_to_onnx(self):
        """
        Saves a sentence transformers model as ONNX
        """

        logging.info("Initializing model object...")
        model_id = self.model
        model_path = Path(self.onnx_model_path)

        # load vanilla transformers and convert to onnx
        model = ORTModelForFeatureExtraction.from_pretrained(model_id, from_transformers=True)
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)

        logging.info("Converting model to ONNX...")
        # save onnx checkpoint and tokenizer
        model.save_pretrained(model_path)
        self.tokenizer.save_pretrained(model_path)


if __name__ == "__main__":
    ONNXConverter().convert_to_onnx()
