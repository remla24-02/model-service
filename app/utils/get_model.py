"""
Download and extract training, testing and validation data.
"""
import os
import subprocess

from utils.logging import AppLogger

logger = AppLogger.__call__().get_logger()


def fetch_model(tag, output_path):
    """
    Fetches a model from a specified URL and saves it to the given output path.

    Args:
        tag (str): The tag or version of the model to fetch.
        output_path (str): The path where the fetched model will be saved.

    Returns:
        None
    """
    url = "https://github.com/remla24-02/model-training.git"
    model_path = "models/trained_model.joblib"
    try:
        subprocess.run(["dvc", "get", url, model_path,
                       "-o", output_path, "--rev", tag, "--force"], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to fetch model from {url}.")
        logger.error(e)
        raise e


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
