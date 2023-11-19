import logging
import logging.config
from datetime import datetime
from pathlib import Path

import pytz
from botocore.exceptions import ClientError

from src.conf.config_manager import ConfigManager


class ModelStore:
    """
    Uploads, downloads, and returns metadata about
    viberary sentence-transformer models
    versioned based on y-m-d-hh format.
    """

    def __init__(self, s3_client):
        self.client = s3_client

        self.cm = ConfigManager()
        self.root_dir = self.cm.get_root_dir()
        self.conf = ConfigManager().get_config_file()
        self.local_dir = Path(self.root_dir) / self.conf["model"]["onnx_path"]
        self.bucket = self.conf["spaces"]["bucket_name"]
        self.logger_path = self.cm.get_logger_path()
        logging.config.fileConfig(self.logger_path)

    def _set_time(self) -> str:
        timezone_str = "UTC"
        tz = pytz.timezone(timezone_str)
        today_date = datetime.now(tz)
        return today_date.strftime("%y-%m-%d-%H")

    def get_model_metadata(self, s3_prefix: str):
        for obj in self.client.list_objects_v2(Bucket=self.bucket, Prefix=s3_prefix)["Contents"]:
            logging.info(obj)
            print(f"{obj}")

    def download_model_dir(self, s3_prefix: str) -> None:
        try:
            local_path = Path(self.local_dir) / s3_prefix
            local_path.mkdir(parents=True, exist_ok=True)
            print(f"Creating {local_path}")

            for obj in self.client.list_objects_v2(Bucket=self.bucket, Prefix=s3_prefix)[
                "Contents"
            ]:
                print(f"Reading {obj}")
                local_file_path = local_path / Path(obj["Key"]).name
                self.client.download_file(self.bucket, obj["Key"], str(local_file_path))

            logging.info("Directory '{self.s3_prefix}' downloaded to '{self.local_path}' ")

        except ClientError as e:
            logging.error(e)

    def upload_model_dir(self, local_path: str) -> None:
        # set model artifact date to generated hour
        s3_prefix = self._set_time()

        try:
            local_path = Path(local_path)
            for file_path in local_path.rglob("*"):
                if file_path.is_file():
                    relative_path = file_path.relative_to(local_path)
                    s3_key = Path(s3_prefix) / relative_path

                    self.client.upload_file(str(file_path), self.bucket, str(s3_key))
                    print(f"Uploaded {file_path} to s3://{self.bucket}/{s3_key}")

            logging.info("Upload successful")

        except ClientError as e:
            logging.error(e)
