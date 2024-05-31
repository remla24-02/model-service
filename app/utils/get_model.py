"""
Download and extract training, testing and validation data.
"""

import os
import boto3
from botocore import UNSIGNED
from botocore.client import Config
import requests

from utils.logging import AppLogger

logger = AppLogger.__call__().get_logger()


def download_data(bucket_name, file_name, output_file):
    """
    Download data from S3 bucket.
    """
    s3 = boto3.client('s3', region_name='eu-north-1',
                      config=Config(signature_version=UNSIGNED))
    s3.download_file(bucket_name, file_name, output_file)


def get_dvc_file():
    """
    Get the content of a file from a GitHub repository.
    """
    url = 'https://raw.githubusercontent.com/remla24-02/model-training/main/models/trained_model.joblib.dvc'
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Error fetching file: {response.status_code}")


def get_model():
    """
    Main function.
    """
    bucket_name = 'dvc-remla24-02'

    file = get_dvc_file()
    md5_hash = file.split(' ')[2]
    key = 'data/files/md5/' + md5_hash[:2] + '/' + md5_hash[2:]

    if os.path.exists('model/key.txt'):
        with open('model/key.txt', 'r') as f:
            old_key = f.read()

        if old_key == key:
            logger.info('Model is up to date.')
            return

    # store key to compare on next run
    with open('model/key.txt', 'w') as f:
        f.write(key)

    os.makedirs(os.path.join('model'), exist_ok=True)

    download_data(bucket_name, key.rstrip('\n'),
                  os.path.join('model', 'trained_model.joblib'))

    logger.info("Model downloaded.")


if __name__ == '__main__':
    get_model()
