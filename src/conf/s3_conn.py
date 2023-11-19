import os

import boto3
import botocore

from src.conf.config_manager import ConfigManager


class S3Client:
    def __init__(self):
        self.config = ConfigManager().get_config_file()

    def conn(self) -> boto3.client:
        session = boto3.Session(
            aws_access_key_id=os.environ.get("SPACES_ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("SPACES_PRIVATE_KEY"),
        )

        client = session.client(
            "s3",
            endpoint_url=self.config["spaces"]["endpoint_url"],
            config=botocore.config.Config(s3={"addressing_style": "virtual"}),
            region_name=self.config["spaces"]["region_name"],
        )

        return client
