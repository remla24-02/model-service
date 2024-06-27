import os
import subprocess
import boto3
import yaml
import sys
from botocore import UNSIGNED
from botocore.config import Config
from utils.logging import AppLogger

logger = AppLogger.__call__().get_logger()


def download_data(bucket_name, file_name, output_file):
    """
    Pull specific files from the DVC remote storage.
    """
    s3 = boto3.client('s3', region_name='eu-north-1',
                      config=Config(signature_version=UNSIGNED))
    try:
        s3.download_file(bucket_name, file_name, output_file)
        print(f"Successfully downloaded {file_name} to {output_file}")
    except Exception as e:
        print(f"Error downloading {file_name}: {e}")
        sys.exit(1)


def fetch_dvc_lock(tag, repo_url='https://github.com/remla24-02/model-training.git'):
    """
    Fetches the dvc.lock file from the specified repo and tag.

    Args:
        tag (str): The git tag to fetch the dvc.lock file from.
        repo_url (str): The URL of the git repository.

    Returns:
        dict: The contents of the dvc.lock file as a dictionary.
    """
    try:
        subprocess.run(["git", "clone", repo_url, "--branch",
                       tag, "--single-branch", "temp_repo"], check=True)
        with open(os.path.join("temp_repo", "dvc.lock"), 'r', encoding='utf-8') as file:
            dvc_lock_data = yaml.safe_load(file)
        # Clean up the cloned repo
        subprocess.run(["rm", "-rf", "temp_repo"], check=True)
        return dvc_lock_data
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to fetch dvc.lock from {repo_url}.")
        logger.error(e)
        raise e


def fetch_model(tag, output_path):
    """
    Fetches the model from the DVC remote storage using the dvc.lock file.

    Args:
        tag (str): The git tag to fetch the model from.
        output_path (str): The path where the fetched model will be saved.

    Returns:
        None
    """
    dvc_lock_data = fetch_dvc_lock(tag)

    # Locate the trained model path and md5 hash in the dvc.lock file
    for stage in dvc_lock_data['stages'].values():
        for out in stage.get('outs', []):
            if out['path'] == 'models/trained_model.joblib':
                md5_hash = out['md5']
                key = f'data/files/md5/{md5_hash[:2]}/{md5_hash[2:]}'
                bucket_name = 'dvc-remla24-02'

                # Ensure directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                download_data(bucket_name, key, output_path)
                return

    logger.error(
        "The specified model path 'models/trained_model.joblib' was not found in dvc.lock")
    raise FileNotFoundError(
        "The specified model path 'models/trained_model.joblib' was not found in dvc.lock")


def get_model():
    """
    Main function.
    """
    model_tag = os.getenv("MODEL_TAG")

    if not model_tag:
        raise ValueError("MODEL_TAG environment variable is not set")

    if model_tag != "stable" and model_tag != "canary":
        model_tag = "stable"

    fetch_model(model_tag, os.path.join('model', 'trained_model.joblib'))

    logger.info("Model downloaded.")


if __name__ == '__main__':
    get_model()
