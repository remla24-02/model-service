"""
Download and extract training, testing and validation data.
"""

import os
import boto3
from botocore import UNSIGNED
from botocore.client import Config


def download_data(bucket_name, file_name, output_file):
    """
    Download data from S3 bucket.
    """
    s3 = boto3.client('s3', region_name='eu-north-1',
                      config=Config(signature_version=UNSIGNED))
    s3.download_file(bucket_name, file_name, output_file)


def get_model():
    """
    Main function.
    """
    bucket_name = 'dvc-remla24-02'
    key = 'data/files/md5/8d/f32b50c3e19897d9b981ae186dfd78'

    download_data(bucket_name, key.rstrip('\n'),
                  os.path.join('model', 'trained_model.joblib'))


if __name__ == '__main__':
    get_model()
